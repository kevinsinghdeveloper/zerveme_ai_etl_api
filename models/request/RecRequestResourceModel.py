from dataclasses import dataclass
from typing import Optional

from abstractions.models.RequestResourceModel import RequestResourceModel


@dataclass
class RecRequestResourceModel(RequestResourceModel):
    product_title: Optional[str]
    #web_site: Optional[str]