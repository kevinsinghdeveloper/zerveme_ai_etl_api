from dataclasses import dataclass
from typing import Optional, List

from abstractions.models.RequestResourceModel import RequestResourceModel


@dataclass
class LLMRequestResourceModel(RequestResourceModel):
    system_prompt: str
    prompt: str
    examples: Optional[str] = None  # Optional examples to guide the LLM
    response_type: Optional[str] = None
    history_messages: Optional[List[str]] = None

