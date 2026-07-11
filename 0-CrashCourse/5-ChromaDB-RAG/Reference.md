# ChromaDB RAG Reference

This folder uses:

```txt
openai==2.44.0
python-dotenv==1.2.2
chromadb==1.5.9
```

## 1. Create An OpenAI Client

Syntax:

```python
client = OpenAI(
    base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)
```

Example:

```python
def create_client() -> OpenAI:
    load_dotenv(Path(__file__).with_name(".env"), override=True)
    return OpenAI(base_url=os.environ["AZURE_OPENAI_ENDPOINT"], api_key=os.environ["AZURE_OPENAI_API_KEY"])
```

## 2. Create Embeddings

Syntax:

```python
response = client.embeddings.create(
    model=os.environ["Embedding_Model"],
    input=text,
)
embedding = response.data[0].embedding
```

Example:

```python
def embed(client: OpenAI, text: str) -> list[float]:
    response = client.embeddings.create(model=os.environ["Embedding_Model"], input=text)
    return response.data[0].embedding
```

## 3. Create A Chroma Collection

Syntax:

```python
import chromadb

chroma = chromadb.Client()
collection = chroma.get_or_create_collection("collection_name")
```

Example:

```python
chroma = chromadb.Client()
collection = chroma.get_or_create_collection("crash_course_rag")
```

## 4. Add Documents To ChromaDB

Syntax:

```python
collection.add(
    ids=["doc-1"],
    documents=["document text"],
    embeddings=[embedding],
)
```

Example:

```python
collection.add(
    ids=[f"doc-{index}" for index, _ in enumerate(DOCUMENTS)],
    documents=DOCUMENTS,
    embeddings=[embed(client, text) for text in DOCUMENTS],
)
```

## 5. Retrieve Documents

Syntax:

```python
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2,
)
documents = results["documents"][0]
```

Example:

```python
results = collection.query(
    query_embeddings=[embed(client, question)],
    n_results=2,
)
context = "\n".join(results["documents"][0])
```

## 6. RAG Answer Generation

Syntax:

```python
response = client.chat.completions.create(
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    messages=[
        {"role": "system", "content": "Answer only from the provided context."},
        {"role": "user", "content": f"Question: {question}\nContext:\n{context}"},
    ],
)
```

Example:

```python
response = client.chat.completions.create(
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    messages=[
        {"role": "system", "content": "Answer only from the provided context."},
        {"role": "user", "content": f"Question: {question}\nContext:\n{context}"},
    ],
)
print(response.choices[0].message.content)
```

## 7. Multi-Agent RAG Orchestration

Syntax:

```python
context = retriever_agent(client, question)
answer = answer_agent(client, question, context)
review = reviewer_agent(client, answer)
```

Example:

```python
context = retriever_agent(client, "How should suspicious access be classified?")
answer = answer_agent(client, question, context)
review = reviewer_agent(client, answer)
```
