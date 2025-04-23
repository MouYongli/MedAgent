import os

import evaluate
import numpy as np
from typing import List, Dict

from dotenv import load_dotenv

from general.data_model.question_dataset import ExpectedAnswer
from general.helper.embedder import OpenAIEmbedder

load_dotenv(dotenv_path="../../../.local-env")

embedder = OpenAIEmbedder(
    api_key = os.getenv("AZURE_OPENAI_API_KEY"),
    api_base = os.getenv("AZURE_OPENAI_API_BASE"),
    api_version = os.getenv("AZURE_OPENAI_API_VERSION"),
    deployment_name = "text-embedding-3-large"
)

rouge = evaluate.load("rouge")  # https://huggingface.co/spaces/evaluate-metric/rouge
bleu = evaluate.load("bleu")  # https://huggingface.co/spaces/evaluate-metric/bleu
meteor = evaluate.load("meteor")  # https://huggingface.co/spaces/evaluate-metric/meteor

def embedding_cosine_similarity(text1: str, text2: str) -> float:
    embedding_1 = np.array(embedder.embed(text1))
    embedding_2 = np.array(embedder.embed(text2))
    return float(np.dot(embedding_1, embedding_2) / (np.linalg.norm(embedding_1) * np.linalg.norm(embedding_2)))

def create_accuracy_scores(
        expected_retrieval: List[ExpectedAnswer],
        provided_answer: str
) -> Dict[str, float]:
    """
    Evaluates the accuracy of a provided answer by comparing it to the expected retrieval using various metrics such as ROUGE, BLEU, METEOR, and cosine similarity of embeddings.

    :param expected_retrieval: A list of `ExpectedAnswer` instances representing
        the expected answers to be compared against.
    :param provided_answer: A string containing the answer provided by the model
        or system that needs to be evaluated.
    :return: A dictionary containing the following key-value pairs with all values in [0, 1] range:
        - "ROUGE-1": The computed ROUGE-1 score; recall of uni-grams (got relevant content?)
        - "ROUGE-L": The computed ROUGE-L score; recall of longest n-gram
        - "BLEU": The computed BLEU score; precision of n-grams (how relevant is content?)
        - "METEOR": The computed METEOR score; f1 with synonoyms / stems (got relevant content and measure relevance of content)
        - "Embedding similarity": The scaled computed cosine similarity between embeddings of the provided answer and expected answer; semantic similarity
    """
    expected_answer = "; ".join([er.text for er in expected_retrieval])

    if provided_answer is not None and expected_answer is not None:
        bleu_score = bleu.compute(predictions=[provided_answer], references=[[expected_answer]])["bleu"]
        rouge_scores = rouge.compute(predictions = [provided_answer], references = [expected_answer])
        rouge_1_score = rouge_scores[f"rouge1"]
        rouge_l_score = rouge_scores[f"rougeL"]
        meteor_score = meteor.compute(predictions = [provided_answer], references = [expected_answer])[f"meteor"]
        emb_cos_sim = embedding_cosine_similarity(provided_answer, expected_answer)
        scaled_emb_sim = (emb_cos_sim + 1) / 2
    else:
        bleu_score = 0.0
        rouge_1_score = 0.0
        rouge_l_score = 0.0
        meteor_score = 0.0
        scaled_emb_sim = 0.0

    return {
        "ROUGE-1": rouge_1_score,
        "ROUGE-L": rouge_l_score,
        "BLEU": bleu_score,
        "METEOR": meteor_score,
        "Embedding similarity": scaled_emb_sim
    }