from agents import Agent, RunConfig, Runner
from pydantic import BaseModel, Field

from config.settings import get_chat_model


class DecomposedQuestions(BaseModel):
    questions: list[str] = Field(min_length=3, max_length=3)


def decompose_question(question: str, run_config: RunConfig) -> list[str]:
    agent = Agent(
        name="Query Decomposition Agent",
        instructions=(
            "Break the user's complex question into exactly three focused retrieval "
            "sub-questions. Each sub-question must cover one distinct information need."
        ),
        model=get_chat_model(),
        output_type=DecomposedQuestions,
    )
    result = Runner.run_sync(agent, question, run_config=run_config, max_turns=1)
    return result.final_output.questions


def synthesize_answer(
    question: str,
    sub_questions: list[str],
    retrieved_chunks,
    run_config: RunConfig,
) -> str:
    context = "\n\n".join(
        f"Sub-question: {chunk.sub_question}\nSource: {chunk.citation()}\nContent: {chunk.text}"
        for chunk in retrieved_chunks
    )
    agent = Agent(
        name="Query Decomposition RAG Synthesis Agent",
        instructions=(
            "Combine evidence retrieved for multiple sub-questions into one grounded answer. "
            "Answer the original question completely and cite the supplied PDF sources."
        ),
        model=get_chat_model(),
    )
    prompt = (
        f"Original question:\n{question}\n\nSub-questions:\n{sub_questions}\n\n"
        f"Retrieved evidence:\n{context}\n\nFinal answer:"
    )
    result = Runner.run_sync(agent, prompt, run_config=run_config, max_turns=1)
    return str(result.final_output)
