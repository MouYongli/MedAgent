from typing import List
from app.dependencies.neo4j_driver import get_neo4j_driver
from app.dependencies.tf_matrix import load_tf_matrix
from app.schemas.chunk import Chunk
from app.dependencies.para_chunks import load_para_chunks
from app.utils.neo4j_util import Neo4jHandler
from igraph import Graph
import numpy as np
import spacy
from scispacy.linking import EntityLinker

from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer


class KnowledgeGraph:
    num_nodes: int
    edges: List
    node_names: List

    def __init__(self, entities_list, global_triples):
        self.num_nodes = len(entities_list)
        self.edges = [
            (triple["source"]["id"], triple["destination"]["id"])
            for triple in global_triples
        ]
        self.node_names = [entity["name"] for entity in entities_list]

    def get_graph(self):
        graph = Graph(directed=True)
        graph.add_vertices(self.num_nodes)
        if self.node_names:
            graph.vs["name"] = self.node_names
        graph.add_edges(self.edges)
        return graph


class GraphRetriever:
    def __init__(self, K, tf_matrix, driver, graph, num_nodes):
        self.nlp = spacy.load("en_core_sci_scibert")  # spacy.load("en_core_sci_sm") #
        # self.nlp.add_pipe(
        #     "scispacy_linker",
        #     config={"resolve_abbreviations": True, "linker_name": "umls"},
        # )

        self.model = SentenceTransformer(
            "neuml/pubmedbert-base-embeddings", device="cpu"
        )
        self.top_K = K
        self.driver = driver
        self.graph = graph
        self.tf_matrix = tf_matrix
        self.num_nodes = graph.vcount()
        self.passage_matrix = []
        for tf_vec in self.tf_matrix:
            passage_vec = [0] * self.num_nodes
            for ind in tf_vec:
                passage_vec[ind] = 1
            self.passage_matrix.append(passage_vec)
        self.passage_matrix = np.array(self.passage_matrix)

    def _extract_query_entities(self, query):
        entities = self.nlp(query).ents
        query_entities = [str(ent.text) for ent in entities]
        return query_entities

    def _query_similar_by_name(self, tx, name):
        embedding = self.model.encode(name).tolist()

        query = """
        CALL db.index.vector.queryNodes('entityEmbedding', $top_k, $embedding)
        YIELD node AS entity, score
        RETURN entity.name AS name, entity.cui AS cui, entity.id AS id, score
        """
        return tx.run(query, top_k=self.top_K, embedding=embedding).data()

    def get_query_vector(self, query):
        query_nodes = []
        query_entities = self._extract_query_entities(query)
        ## DEBUG start ##
        print(f"Query entities: {query_entities}")
        ## DEBUG end ##
        with self.driver.session() as session:
            for entity in query_entities:
                results = session.read_transaction(self._query_similar_by_name, entity)
                query_nodes.append(results[0])
        query_entity_ids = [obj["id"] for obj in query_nodes]
        # print(f"Query entity ids: {query_entity_ids}")
        query_vector = [0] * self.num_nodes
        for id in query_entity_ids:
            query_vector[id] = 1
        # DEBUG Start #
        # print("Query vector before PPR")
        # print(query_vector)
        # DEBUG END #
        # print()
        return query_vector

    def get_query_vector_optim(self, query):
        query_entities = self._extract_query_entities(query)
        print(f"Query entities: {query_entities}")

        # Batch encode all entity names
        embeddings = self.model.encode(query_entities).tolist()

        # Batch Neo4j query
        def batch_query(tx, names, embeddings):
            results = []
            for name, embedding in zip(names, embeddings):
                query = """
                CALL db.index.vector.queryNodes('entityEmbedding', $top_k, $embedding)
                YIELD node AS entity, score
                RETURN entity.name AS name, entity.cui AS cui, entity.id AS id, score
                """
                res = tx.run(query, top_k=self.top_K, embedding=embedding).data()
                if res:
                    results.append(res[0])
            return results

        with self.driver.session() as session:
            query_nodes = session.read_transaction(
                batch_query, query_entities, embeddings
            )

        query_entity_ids = [obj["id"] for obj in query_nodes if obj]
        query_vector = [0] * self.num_nodes
        for id in query_entity_ids:
            query_vector[id] = 1
        return query_vector

    def get_ppr_vector(self, query):
        query_vector = self.get_query_vector_optim(query)

        ppr_vector = self.graph.personalized_pagerank(reset=query_vector, damping=0.85)
        ppr_vector = np.array(ppr_vector)
        return ppr_vector

    def retrieve_chunk_ids(self, query):
        query_vector = self.get_ppr_vector(query)
        # Debug
        print("Query vector after PPR ")
        print(query_vector)
        # Debug
        passage_matrix = self.passage_matrix

        # Calculate similarity scores
        scores = np.dot(passage_matrix, query_vector)
        top_K_indices = np.argsort(scores)[-self.top_K :][::-1]

        # Convert indices to chunk IDs
        top_K_chunks = [int(index) for index in top_K_indices]
        return top_K_chunks

    def retrieve_chunks(self, query):
        top_K_chunks = self.retrieve_chunk_ids(query)
        para_chunks = load_para_chunks()
        chunks = []
        for id in top_K_chunks:
            chunks.append(
                Chunk(
                    page_content=para_chunks[id].page_content,
                    book_name=para_chunks[id].book_name,
                    page_number=para_chunks[id].page_number,
                    id=id,
                )
            )
        # return "\n\n".join(chunks)
        print("Graph RAG Retriever finished")
        return chunks


_graph_retriever = None


def get_graph_retriever(top_k: int = 5):
    global _graph_retriever
    from app.dependencies.graph_retriever import (
        GraphRetriever,
    )  # Avoid circular import

    if _graph_retriever is None or _graph_retriever.top_K != top_k:
        neo4j_handler = Neo4jHandler()
        entities_list = neo4j_handler.get_all_entities()
        num_nodes = len(entities_list)
        global_triples = neo4j_handler.get_all_relationships()
        knowledge_graph = KnowledgeGraph(entities_list, global_triples)

        graph = knowledge_graph.get_graph()
        _graph_retriever = GraphRetriever(
            K=5,
            tf_matrix=load_tf_matrix(),
            driver=get_neo4j_driver(),
            graph=graph,
            num_nodes=num_nodes,
        )
    return _graph_retriever
