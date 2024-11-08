from typing import List, Tuple, Union

from models.request.RecRequestResourceModel import RecRequestResourceModel
from models.response.SerpResponseModel import SerpResponseModel
from utility.Utility import Utility


class RecommendationEngineManager:
    def __init__(self):
        pass

    def find_same_product(self, product_resource: RecRequestResourceModel,
                          related_products: List[SerpResponseModel],
                          related_product_name_field: str,
                          price_difference_range: Tuple[float, float] = None) -> Union[SerpResponseModel | None]:
        # TODO find same product at lower price
        related_products_df = Utility.dataclass_to_dataframe(related_products)

        # TODO fuzzy match to locate

        # price_difference_range -> .3 to .6 (30 - 60 % diff) -> not required here -> just find at lower price
        return None

    def find_related_product(self, product_resource: RecRequestResourceModel,
                             related_products: List[SerpResponseModel],
                             related_product_name_field: str,
                             price_difference_range: Tuple[float, float]) -> Union[SerpResponseModel | None]:
        # TODO find similar product at lower price
        related_products_df = Utility.dataclass_to_dataframe(related_products)


        # price_difference_range -> .3 to .6 (30 - 60 % diff)
        return None

