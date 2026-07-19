from config.settings import get_embedding_model


# This service creates vector embeddings for semantic search.
# Embeddings allow ChromaDB to find support chunks that are close in meaning to
# the user's question, even when exact words do not match.


# Function: create one embedding vector for the provided text.
# Logic:
# 1. Read the embedding model name from this lab's local .env file.
# 2. Send the text to Azure OpenAI embeddings.
# 3. Return the first embedding vector from the response.
def create_embedding(client, text: str) -> list[float]:
    response = client.embeddings.create(
        model=get_embedding_model(),
        input=text,
    )
    return response.data[0].embedding
