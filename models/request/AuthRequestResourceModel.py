from dataclasses import dataclass
from typing import Optional

from abstractions.models.RequestResourceModel import RequestResourceModel


@dataclass
class AuthRequestResourceModel(RequestResourceModel):
    user_key: Optional[str]
    #web_site: Optional[str]