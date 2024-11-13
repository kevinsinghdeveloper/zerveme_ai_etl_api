from dataclasses import dataclass
from typing import Optional

from abstractions.models.ResponseModel import ResponseModel


@dataclass
class SerpResponseModel(ResponseModel):
    product_title: Optional[str]
    product_id: Optional[str]
    url: Optional[str]
    merchant: Optional[str]
    price: Optional[float]
    position_rank: Optional[int]
    rating: Optional[float]
    reviews: Optional[int]
    product_image: Optional[str]