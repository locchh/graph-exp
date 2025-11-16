import os
from neo4j import Driver
import openai


def execute_query(driver: Driver, query: str, parameters: dict = None):
    with driver.session() as session:
        result = session.run(query, parameters)
        return result.data()


def create_embedding(text: str):
    """Create embedding for text using OpenAI"""
    if not text or not text.strip():
        return None
    
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error creating embedding: {e}")
        return None