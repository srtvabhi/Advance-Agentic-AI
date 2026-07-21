from agents import Agent, RunConfig, Runner

from config.settings import get_chat_model


def detect_product_filter(question: str) -> str | None:
    lowered = question.lower()
    if "analyticspro" in lowered or "analytics pro" in lowered:
        return "AnalyticsPro"
    if "securepay" in lowered or "secure pay" in lowered:
        return "SecurePay"
    return None


def answer_with_hybrid_context(
    question: str,
    results,
    run_config: RunConfig,
) -> str:
    context = "\n\n".join(
        f"Search type: {item.search_type}\nScore: {item.score:.3f}\n"
        f"Source: {item.citation()}\nContent: {item.text}"
        for item in results
    )
    agent = Agent(
        name="Hybrid Search Support Agent",
        instructions=(
            "Answer support questions only from the supplied hybrid-search context. "
            "Combine semantic and exact-keyword evidence, explain the resolution simply, "
            "and include citations. State when the context is insufficient."
        ),
        model=get_chat_model(),
    )
    prompt = f"Question:\n{question}\n\nHybrid search context:\n{context}\n\nAnswer:"
    result = Runner.run_sync(agent, prompt, run_config=run_config, max_turns=1)
    return str(result.final_output)
