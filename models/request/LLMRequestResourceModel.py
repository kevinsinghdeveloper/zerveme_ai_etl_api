from dataclasses import dataclass
from typing import Optional

from abstractions.models.RequestResourceModel import RequestResourceModel


@dataclass
class LLMRequestResourceModel(RequestResourceModel):
    system_prompt: str
    instructions_prompt: str # Instructions for the LLM to follow
    prompt: str
    examples: Optional[str] = None  # Optional examples to guide the LLM
