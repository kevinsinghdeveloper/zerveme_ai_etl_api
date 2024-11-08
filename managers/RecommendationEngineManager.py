from typing import List, Tuple, Union

from models.response.SerpResponseModel import SerpResponseModel


class RecommendationEngineManager:
    def __init__(self):
        pass

    def find_same_product(self, source_product_name: str,
                          related_products: List[SerpResponseModel],
                          price_difference_range: Tuple[float, float] = None) -> Union[SerpResponseModel | None]:
        # TODO find same product at lower price

        # price_difference_range -> .3 to .6 (30 - 60 % diff) -> not required here -> just find at lower price
        pass

    def find_related_product(self, source_product_name: str,
                             related_products: List[SerpResponseModel],
                             price_difference_range: Tuple[float, float]) -> Union[SerpResponseModel | None]:
        # TODO find similar product at lower price

        # price_difference_range -> .3 to .6 (30 - 60 % diff)
        pass

