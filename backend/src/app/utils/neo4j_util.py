from app.dependencies.neo4j_driver import get_neo4j_driver
from neo4j import GraphDatabase
from configparser import ConfigParser
import pickle
from tqdm import tqdm


class Neo4jHandler:
    def __init__(self):
        self.driver = get_neo4j_driver()

    def close(self):
        self.driver.close()

    def create_node(self, label, properties):
        with self.driver.session() as session:
            session.write_transaction(self._create_node, label, properties)

    @staticmethod
    def _create_node(tx, label, properties):
        query = f"CREATE (n:{label} {{"
        query += ", ".join([f"{key}: ${key}" for key in properties.keys()])
        query += "})"
        tx.run(query, **properties)

    def create_relationship(
        self, label1, properties1, relationship, label2, properties2
    ):
        with self.driver.session() as session:
            session.write_transaction(
                self._create_relationship,
                label1,
                properties1,
                relationship,
                label2,
                properties2,
            )

    @staticmethod
    def _create_relationship(
        tx, label1, properties1, relationship, label2, properties2
    ):
        query = (
            f"MATCH (a:{label1} {{"
            + ", ".join([f"{key}: ${'a_' + key}" for key in properties1.keys()])
            + f"}}), (b:{label2} {{"
            + ", ".join([f"{key}: ${'b_' + key}" for key in properties2.keys()])
            + f"}}) CREATE (a)-[r:{relationship}]->(b)"
        )
        parameters = {f"a_{key}": value for key, value in properties1.items()}
        parameters.update({f"b_{key}": value for key, value in properties2.items()})
        tx.run(query, **parameters)

    @staticmethod
    def _create_vector_index(tx):
        query = """
        CREATE VECTOR INDEX entityEmbedding IF NOT EXISTS
        FOR (n:Entity) ON n.embedding
        OPTIONS { indexConfig: {
        `vector.dimensions`: 768,
        `vector.similarity_function`: 'cosine'
        }}
        """
        tx.run(query)

    def create_vector_index(self):
        with self.driver.session() as session:
            session.write_transaction(self._create_vector_index)

    def get_all_entities(self):
        """Retrieve all nodes with the label 'Entity'."""
        with self.driver.session() as session:
            result = session.execute_read(self._get_all_entities)
            return result

    @staticmethod
    def _get_all_entities(tx):
        query = "MATCH (n:Entity) RETURN n"
        entities = [record["n"] for record in tx.run(query)]
        entities_lite = []
        for entity in entities:
            entity_lite = {}
            entity_lite["name"] = entity.get("name")
            entity_lite["id"] = entity.get("id")
            entities_lite.append(entity_lite)
        # len(entities_lite) --> gives num of entities
        return entities_lite  # gives sorted list

    def get_all_relationships(self):
        """Retrieve all relationships between nodes with the label 'Entity'."""
        with self.driver.session() as session:
            result = session.execute_read(self._get_all_relationships)
            return result

    @staticmethod
    def _get_all_relationships(tx):
        query = """
        MATCH (a:Entity)-[r]->(b:Entity)
        RETURN a.id AS source_id, a.name AS source_name, 
               type(r) AS relationship, 
               b.id AS target_id, b.name AS target_name
        """
        relationships = [record.data() for record in tx.run(query)]
        relationships_lite = []
        for rel in relationships:
            rel_lite = {"source": {}, "destination": {}}
            rel_lite["source"] = {
                "id": rel.get("source_id"),
                "name": rel.get("source_name"),
            }
            rel_lite["destination"] = {
                "id": rel.get("target_id"),
                "name": rel.get("target_name"),
            }
            relationships_lite.append(rel_lite)
        return relationships_lite

    def store_tf_matrix(self, tf_matrix):  # can store matrix but too many relationships
        """
        Store the term frequency matrix in Neo4j as an isolated subgraph.
        Each chunk is represented as a node with label 'Chunk' and properties from the corresponding dict in chunks_list.
        Each entity is represented as a node with label 'TFEntity' and property 'id'.
        A relationship (:MENTIONS) is created from each Chunk to the TFEntity nodes it mentions.
        """
        with self.driver.session() as session:
            for chunk_id, entity_ids in tqdm(enumerate(tf_matrix)):
                for entity_id in entity_ids:
                    # Create or merge the entity node with label 'TFEntity'
                    session.run(
                        "MERGE (e:TFEntity {id: $entity_id})", entity_id=entity_id
                    )
                    # Create relationship from chunk to entity
                    session.run(
                        """
                        MATCH (c:Chunk {id: $chunk_id}), (e:TFEntity {id: $entity_id})
                        MERGE (c)-[:MENTIONS]->(e)
                        """,
                        chunk_id=chunk_id,
                        entity_id=entity_id,
                    )
        print("Stored tf matrix to neo4j")

    def get_tf_matrix(self):
        """
        Retrieve the term frequency matrix from Neo4j.
        Returns a list of lists, where each sublist contains the entity ids mentioned by a chunk,
        ordered by the chunk's id.
        """
        with self.driver.session() as session:
            result = session.execute_read(self._get_tf_matrix)
            return result

    @staticmethod
    def _get_tf_matrix(tx):
        # Get all Chunk nodes and their mentioned TFEntity ids
        query = """
        MATCH (c:Chunk)
        OPTIONAL MATCH (c)-[:MENTIONS]->(e:TFEntity)
        RETURN c.id AS chunk_id, collect(e.id) AS entity_ids
        ORDER BY chunk_id
        """
        tf_matrix = []
        for record in tx.run(query):
            # Filter out None values if there are chunks with no entities
            entity_ids = [eid for eid in record["entity_ids"] if eid is not None]
            tf_matrix.append(entity_ids)
        return tf_matrix

    def get_chunk_by_index(self, index):
        """
        Retrieve the properties of a Chunk node by its index (id).
        Returns a dictionary of properties if found, else None.
        """
        with self.driver.session() as session:
            result = session.run("MATCH (c:Chunk {id: $index}) RETURN c", index=index)
            record = result.single()
            if record:
                return dict(record["c"])
            return None
