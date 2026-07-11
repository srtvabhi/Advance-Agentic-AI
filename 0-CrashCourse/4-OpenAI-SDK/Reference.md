# OpenAI SDK Reference

This folder uses:

```txt
openai==2.44.0
python-dotenv==1.2.2
```

## 1. Create A Client

Syntax:

```python
from openai import OpenAI

client = OpenAI(
    base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)
```

Example:

```python
def create_client() -> OpenAI:
    load_dotenv(Path(__file__).with_name(".env"), override=True)
    return OpenAI(
        base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )
```

## 2. Single Agent Syntax

Syntax:

```python
response = client.chat.completions.create(
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    messages=[
        {"role": "system", "content": "Agent instructions."},
        {"role": "user", "content": user_question},
    ],
)
answer = response.choices[0].message.content
```

Example:

```python
response = client.chat.completions.create(
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    messages=[
        {"role": "system", "content": "You are a concise assistant."},
        {"role": "user", "content": "Explain the OpenAI SDK."},
    ],
)
print(response.choices[0].message.content)
```

## 3. Tool Calling Pattern

Syntax:

```python
tool_result = tool_function(user_question)
response = client.chat.completions.create(
    model=model_name,
    messages=[
        {"role": "system", "content": "Answer using the tool result."},
        {"role": "user", "content": f"Question: {question}\nTool result: {tool_result}"},
    ],
)
```

Example:

```python
tool_result = calculator("99 / 3")
response = client.chat.completions.create(
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    messages=[
        {"role": "system", "content": "Answer using the provided tool result."},
        {"role": "user", "content": f"Question: Calculate 99 / 3\nTool result: {tool_result}"},
    ],
)
```

## 4. Multi-Agent Orchestration

Syntax:

```python
plan = call_agent(client, "planner instructions", task)
execution = call_agent(client, "executor instructions", plan)
review = call_agent(client, "reviewer instructions", execution)
```

Example:

```python
plan = call_agent(client, "planner", "You are a planner. Create 5 short steps.", task)
execution = call_agent(client, "executor", "You are an executor. Add actions and owners.", plan)
review = call_agent(client, "reviewer", "You are a reviewer. Identify risks and missing approvals.", execution)
```

## 5. Embeddings Syntax

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
embedding = client.embeddings.create(
    model=os.environ["Embedding_Model"],
    input="Remote work policy text",
).data[0].embedding
```
