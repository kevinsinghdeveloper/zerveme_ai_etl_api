from dataclasses import dataclass
from typing import Optional

from abstractions.models.ResponseModel import ResponseModel


@dataclass
class LLMResponseModel(ResponseModel):
    response: str
    usage: Optional[dict] = None
