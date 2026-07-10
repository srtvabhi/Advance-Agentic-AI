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
    return ValidationResult(draft=str(draft), review=str(review), status=status)

