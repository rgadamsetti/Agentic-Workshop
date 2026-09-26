from typing import Literal

from pydantic import BaseModel, field_validator, model_validator

Category = Literal["billing", "bug", "access", "performance", "how-to"]
Priority = Literal["P1", "P2", "P3", "P4"]
Route = Literal[
    "billing-team",
    "bug-team",
    "access-team",
    "performance-team",
    "how-to-team",
]


class TriageDecision(BaseModel):
    category: Category
    priority: Priority
    route: Route
    rationale: str

    @field_validator("rationale")
    @classmethod
    def rationale_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("rationale must not be empty")
        return v

    @model_validator(mode="after")
    def route_matches_category(self) -> "TriageDecision":
        expected = f"{self.category}-team"
        if self.route != expected:
            raise ValueError(
                f"route '{self.route}' does not match category '{self.category}' (expected '{expected}')"
            )
        return self
