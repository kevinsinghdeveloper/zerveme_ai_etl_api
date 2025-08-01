from dataclasses import dataclass

from abstractions.models.ResponseModel import ResponseModel


@dataclass
class RecResponseModel(ResponseModel):
    data: dict
    # TODO unsure what to return since we need to get results from serp
    '''
    product_title: Optional[str]
    product_id: Optional[str]
    url: Optional[str]
    merchant: Optional[str]
    price: Optional[str]
    product_title: Optional[str]
    product_title: Optional[str]
    product_title: Optional[str]
    '''
