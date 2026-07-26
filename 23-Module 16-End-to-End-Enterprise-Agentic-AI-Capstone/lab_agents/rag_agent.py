from langsmith import traceable

from config.settings import create_chat_model


VALID_DOMAINS = {"HR", "Sales", "Marketing", "All"}


# LangGraph node helper:
# Use a LangChain chat model so LangSmith can automatically capture LLM span
# metadata such as latency and token usage.
def invoke_llm(system_prompt: str, user_prompt: str) -> str:
    llm = create_chat_model()
    response = llm.invoke(
        [
            ("system", system_prompt),
            ("user", user_prompt),
        ]
    )
    return str(response.content)


# Agentic RAG step:
# Decide which enterprise knowledge domain should be searched before retrieval.
@traceable(
    name="domain_router_agent",
    run_type="chain",
    process_inputs=lambda inputs: {"question": inputs["question"]},
)
def select_data_domain(question: str) -> str:
    system_prompt = (
        "Route each business question to exactly one enterprise data domain.\n"
        "Valid domains: HR, Sales, Marketing, All.\n"
        "Use HR for employee policy, travel, approval, reimbursement, and people questions.\n"
        "Use Sales for revenue, pipeline, region, product sales, win rate, and deal risks.\n"
        "Use Marketing for campaigns, audience, messaging, demand generation, and adoption.\n"
        "Use All only when the question clearly needs multiple departments.\n"
        "Return only the domain name and no extra text."
    )
    selected = invoke_llm(system_prompt, question).strip()
    for domain in VALID_DOMAINS:
        if domain.lower() == selected.lower():
            return domain
    return "All"


# Agentic RAG step:
# Create a short retrieval plan that explains what evidence should be searched.
@traceable(
    name="retrieval_planner_agent",
    run_type="chain",
    process_inputs=lambda inputs: {
        "question": inputs["question"],
        "selected_domain": inputs["selected_domain"],
    },
)
def create_retrieval_plan(question: str, selected_domain: str) -> str:
    system_prompt = (
        "Create a concise three-bullet retrieval plan for answering an enterprise question. "
        "Explain why the selected HR, Sales, Marketing, or All domain is useful."
    )
    user_prompt = f"Question: {question}\nSelected data domain: {selected_domain}"
    return invoke_llm(system_prompt, user_prompt)


# Agentic RAG step:
# Generate the final answer using only retrieved enterprise context.
@traceable(
    name="grounded_answer_agent",
    run_type="chain",
    process_inputs=lambda inputs: {
        "question": inputs["question"],
        "selected_domain": inputs["selected_domain"],
        "plan": inputs["plan"],
        "retrieved_chunk_count": len(inputs["retrieved_chunks"]),
    },
)
def generate_grounded_answer(
    question: str,
    selected_domain: str,
    plan: str,
    retrieved_chunks,
) -> str:
    context = "\n\n".join(
        f"Source: {chunk.citation()}\nContent: {chunk.text}"
        for chunk in retrieved_chunks
    )
    system_prompt = (
        "Answer only from the retrieved enterprise context. If required context is missing, "
        "state what is missing. Pay close attention to threshold words such as over, under, "
        "between, before, and after. Include short citations and identify the data domain used."
    )
    user_prompt = (
        f"Question:\n{question}\n\nSelected data domain:\n{selected_domain}\n\n"
        f"Retrieval plan:\n{plan}\n\nRetrieved context:\n{context}\n\nAnswer:"
    )
    return invoke_llm(system_prompt, user_prompt)
