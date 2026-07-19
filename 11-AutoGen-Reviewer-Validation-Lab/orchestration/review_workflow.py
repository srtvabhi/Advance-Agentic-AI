from agents.reviewer_agents import create_policy_writer, create_validation_reviewer
from models.validation_models import ValidationResult
from services.validation_service import validate_review


async def run_review_workflow(model_client, task: str) -> ValidationResult:
    writer = create_policy_writer(model_client)
    reviewer = create_validation_reviewer(model_client)

    draft_result = await writer.run(task=task)
    draft = draft_result.messages[-1].content

    review_task = f"Review this policy draft:\n\n{draft}"
    review_result = await reviewer.run(task=review_task)
    review = review_result.messages[-1].content

    status = validate_review(str(review))
    if status == "APPROVED":
        return ValidationResult(draft=str(draft), review=str(review), status=status)

    revision_task = (
        "Revise the policy draft using the reviewer feedback. "
        "Make sure the revised policy explicitly includes purpose, scope, access control, "
        "human approval, logging, risk handling, policy owner, audit evidence, and exception handling.\n\n"
        f"Original task:\n{task}\n\n"
        f"Original draft:\n{draft}\n\n"
        f"Reviewer feedback:\n{review}"
    )
    revised_result = await writer.run(task=revision_task)
    revised_draft = revised_result.messages[-1].content

    final_review_task = f"Review this revised policy draft:\n\n{revised_draft}"
    final_review_result = await reviewer.run(task=final_review_task)
    final_review = final_review_result.messages[-1].content
    final_status = validate_review(str(final_review))

    return ValidationResult(
        draft=str(draft),
        review=str(review),
        status=final_status,
        revised_draft=str(revised_draft),
        final_review=str(final_review),
        revision_performed=True,
    )
