from typing import Literal

from agents import Agent, RunConfig, Runner
from pydantic import BaseModel

from config.settings import get_chat_model


class DomainSelection(BaseModel):
    domain: Literal["HR", "Sales", "Marketing", "All"]


def select_data_domain(question: str, run_config: RunConfig) -> str:
    agent = Agent(
        name="Enterprise Domain Router",
        instructions=(
            "Route each business question to exactly one enterprise data domain. "
            "Use HR for employee policy, travel, approval, reimbursement, and people questions. "
            "Use Sales for revenue, pipeline, region, product sales, win rate, and deal risks. "
            "Use Marketing for campaigns, audience, messaging, demand generation, and adoption. "
            "Use All only when the question clearly needs multiple departments."
        ),
        model=get_chat_model(),
        output_type=DomainSelection,
    )
    result = Runner.run_sync(agent, question, run_config=run_config, max_turns=1)
    return result.final_output.domain


def create_retrieval_plan(question: str, selected_domain: str, run_config: RunConfig) -> str:
    agent = Agent(
        name="Enterprise Retrieval Planner",
        instructions=(
            "Create a concise three-bullet retrieval plan for answering an enterprise question. "
            "Explain why the selected HR, Sales, Marketing, or All domain is useful."
        ),
        model=get_chat_model(),
    )
    prompt = f"Question: {question}\nSelected data domain: {selected_domain}"
    result = Runner.run_sync(agent, prompt, run_config=run_config, max_turns=1)
    return str(result.final_output)


def generate_grounded_answer(
    question: str,
    selected_domain: str,
    plan: str,
    retrieved_chunks,
    run_config: RunConfig,
) -> str:
    context = "\n\n".join(
        f"Source: {chunk.citation()}\nContent: {chunk.text}"
        for chunk in retrieved_chunks
    )
    agent = Agent(
        name="Enterprise RAG Answer Agent",
        instructions=(
            "Answer only from the retrieved enterprise context. If required context is missing, "
            "state what is missing. Pay close attention to threshold words such as over, under, "
            "between, before, and after. Include short citations and identify the data domain used."
        ),
        model=get_chat_model(),
    )
    prompt = (
        f"Question:\n{question}\n\nSelected data domain:\n{selected_domain}\n\n"
        f"Retrieval plan:\n{plan}\n\nRetrieved context:\n{context}\n\nAnswer:"
    )
    result = Runner.run_sync(agent, prompt, run_config=run_config, max_turns=1)
    return str(result.final_output)
