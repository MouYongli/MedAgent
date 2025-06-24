from app.schemas.chat_message import ChatMessage
from typing import List
from app.services.generator_service import (
    generate_text_service,
    call_ollama_api_stream,
)
from app.services.vector_retriever_service import retrieve_chunks_vector_db
import json

# In-memory store for demonstration (not for production)
chat_history: List[ChatMessage] = []


def get_chat_history_service() -> List[ChatMessage]:
    return chat_history


def send_message_service(message: str) -> dict:
    chat_history.append(ChatMessage(sender="user", content=message))
    response = {}
    chunks = retrieve_chunks_vector_db(message)
    print(f"Retrieved {len(chunks)} chunks for message: {message}")
    response["chunks"] = chunks
    user_prompt = """Context: \n"""
    for i, chunk in enumerate(chunks):
        user_prompt += f"{i + 1}: {chunk.page_content}\n"
    user_prompt += f"Question: {message}\n"
    gen_response = generate_text_service(user_prompt)
    response["result"] = gen_response
    chat_history.append(ChatMessage(sender="assistant", content=gen_response))
    return response


def send_message_stream_service(message: str):
    chat_history.append(ChatMessage(sender="user", content=message))

    chunks = retrieve_chunks_vector_db(message)
    chunk_list = []
    for chunk in chunks:
        chunk_list.append(
            {
                "page_content": chunk.page_content,
                "book_name": chunk.book_name,
                "id": chunk.id,
                "page_number": chunk.page_number,
            }
        )
    # yield {"type": "chunks", "chunks": chunk_list}

    user_prompt = """Context: \n"""
    for i, chunk in enumerate(chunks):
        user_prompt += f"{i + 1}: {chunk.page_content}\n"
    user_prompt += f"Query: {message}\n"

    # Use the generator from generate_text_stream_service
    for gen_response in call_ollama_api_stream(user_prompt):
        try:
            gen_response = json.loads(gen_response)
        except json.JSONDecodeError:
            yield {
                "type": "error",
                "content": f"Error decoding JSON response: {gen_response}",
            }

        if gen_response.get("done", False):
            yield {
                "type": "answer",
                "content": gen_response["message"]["content"],
                "done": gen_response["done"],
                "chunks": chunk_list,
            }
        else:
            yield {
                "type": "answer",
                "content": gen_response["message"]["content"],
                "done": gen_response["done"],
            }

    chat_history.append(ChatMessage(sender="assistant", content="Streamed response"))
