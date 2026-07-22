from config.settings import get_embedding_model


# This service creates vector embeddings for text.
# Embeddings convert text into numbers so ChromaDB can compare meaning and
# find policy chunks that are semantically close to the user's question.


# Function: create one embedding for the provided text.
# Logic:
# 1. Read the embedding model name from this lab's .env file.
# 2. Send the text to Azure OpenAI embedding endpoint.
# 3. Return the first embedding vector from the response.
def create_embedding(client, text: str) -> list[float]:
    response = client.embeddings.create(
        model=get_embedding_model(),
        input=text,
    )
    return response.data[0].embedding
