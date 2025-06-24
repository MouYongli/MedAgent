from app.schemas.generate_request import GenerateRequest
from app.schemas.generate_response import GenerateResponse
import requests
from app.config import config
import os

from constants import SYSTEM_PROMPT

OLLAMA_API_URL = config["LLM"]["OLLAMA_API_URL"]


def call_ollama_api(prompt: str, model: str = "llama3.1:70b") -> str:
    # For /api/chat endpoint, typical Ollama expects a 'messages' list
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
    }
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        # Ollama /api/chat returns the result in the 'message' field (dict with 'content')
        result_text = data.get("message", {}).get("content", "")
    except Exception as e:
        result_text = f"Error contacting Ollama API: {str(e)}"
    return result_text


def call_ollama_api_stream(prompt: str, model: str = "llama3.1:70b"):
    """
    Calls the Ollama API with streaming enabled.
    Yields each chunk of the response as it arrives.
    """
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "stream": True,
    }
    try:
        with requests.post(
            OLLAMA_API_URL, json=payload, stream=True, timeout=120
        ) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    # Decode and yield each line/chunk of the streamed response
                    yield line.decode("utf-8")
    except Exception as e:
        yield f"Error contacting Ollama API: {str(e)}"


def generate_text_service(request: str) -> str:
    result_text = call_ollama_api(request)
    return result_text


async def generate_text_stream_service(query: str) -> str:
    """
    Service to handle text generation with streaming response.
    Returns a generator that yields each chunk of the response.
    """

    return call_ollama_api_stream(query)
