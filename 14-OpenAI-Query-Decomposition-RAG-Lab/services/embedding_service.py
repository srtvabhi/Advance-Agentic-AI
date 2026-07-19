from config.settings import get_embedding_model


# This service creates embeddings for document chunks and sub-questions.
# Embeddings turn text into vectors so ChromaDB can find semantically similar
# incident-response content for each decomposed question.


# Function: create one embedding vector for the provided text.
# Logic:
# 1. Read the embedding model name from this lab's local .env file.
# 2. Send the text to the Azure OpenAI embedding endpoint.
# 3. Return the vector from the first embedding result.
def create_embedding(client, text: str) -> list[float]:
    response = client.embeddings.create(
        model=get_embedding_model(),
        input=text,
    )
    return response.data[0].embedding
