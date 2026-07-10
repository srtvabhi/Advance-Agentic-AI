from typing import Literal, TypedDict


RouteName = Literal["business", "technical", "risk", "general"]


class RoutingState(TypedDict, total=False):
    question: str
    route: RouteName
    answer: str
    final_response: str

