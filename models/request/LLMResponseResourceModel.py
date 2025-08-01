from dataclasses import dataclass
from typing import Optional, Union

from abstractions.models.ResponseModel import ResponseModel


@dataclass
class LLMResponseResourceModel(ResponseModel):
    response_content: Optional[Union[str, dict]] = None
    history_messages: Optional[list[dict[str, str]]] = None
    usage_data: Optional[dict] = None
