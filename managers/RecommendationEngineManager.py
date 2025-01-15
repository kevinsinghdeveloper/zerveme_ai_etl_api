from typing import List, Tuple, Union
from models.request.RecRequestResourceModel import RecRequestResourceModel
from models.response.SerpResponseModel import SerpResponseModel
from utility.Utility import Utility
from utility.MachineLearningToolkit import MachineLearningToolkit

SIMILARITY_THRESHOLD = .75  # TODO MOVE TO ML_CONFIG
DISSIMILARITY_THRESHOLD = .25  # TODO MOVE TO ML_CONFIG


class RecommendationEngineManager:
    def __init__(self, ml_config):
        self.__ml_tools = MachineLearningToolkit(ml_config)

    def find_same_product(
            self,
            product_resource: RecRequestResourceModel,
            related_products: List[SerpResponseModel],
            related_product_name_field: str,
            price_difference_range: Tuple[float, float] = None
    ) -> Union[SerpResponseModel, None]:
        """
        Finds the same product at a potentially lower price.

        Arguments:
            product_resource: RecRequestResourceModel - The original product data.
            related_products: List[SerpResponseModel] - A list of related product data.
            related_product_name_field: str - The field name to use for product titles.
            price_difference_range: Tuple[float, float] - Optional range for price difference filtering.

        Returns:
            SerpResponseModel or None - The matching product at a lower price, if found.
        """
        related_products_df = Utility.dataclass_to_dataframe(related_products)

        found_related_products_df = self.__ml_tools.get_product_sbert_sim(product_resource=product_resource,
                                                                          related_product_name_field=
                                                                          related_product_name_field,
                                                                          related_products_df=related_products_df)

        found_related_products_df = found_related_products_df[found_related_products_df["similarity"] >=
                                                              SIMILARITY_THRESHOLD]
        found_related_products_df = found_related_products_df.sort_values(by=['similarity'], ascending=False)

        if price_difference_range:
            min_price_per, max_price_per = price_difference_range
            min_price = product_resource.product_price * min_price_per
            max_price = product_resource.product_price * max_price_per

            mask = (found_related_products_df['price'] > min_price) & (found_related_products_df['price'] < max_price)
            found_related_products_df = found_related_products_df[mask]
        else:
            found_related_products_df = found_related_products_df[found_related_products_df['price'] <
                                                                  product_resource.product_price]

        if found_related_products_df.empty:
            return None

        found_related_products_df = found_related_products_df.head(1)

        found_related_products_df = found_related_products_df.drop(columns=['similarity'], axis=1)

        same_product_lower = Utility.dataframe_to_dataclass(found_related_products_df, SerpResponseModel)

        return same_product_lower[0]

    def find_related_product(
            self,
            product_resource: RecRequestResourceModel,
            related_products: List[SerpResponseModel],
            related_product_name_field: str,
            price_difference_range: Tuple[float, float]
    ) -> Union[SerpResponseModel, None]:
        """
        Finds a related product with a similar name that falls within the specified price difference range.

        Arguments:
            product_resource: RecRequestResourceModel - The original product data.
            related_products: List[SerpResponseModel] - A list of related product data.
            related_product_name_field: str - The field name to use for product titles.
            price_difference_range: Tuple[float, float] - The range of acceptable price differences.

        Returns:
            SerpResponseModel or None - The related product, if found within the price range.
        """

        related_products_df = Utility.dataclass_to_dataframe(related_products)

        found_related_products_df = self.__ml_tools.get_product_sbert_sim(product_resource=product_resource,
                                                                          related_product_name_field=
                                                                          related_product_name_field,
                                                                          related_products_df=related_products_df)

        found_related_products_df = found_related_products_df[found_related_products_df["similarity"] >=
                                                              DISSIMILARITY_THRESHOLD]

        found_related_products_df = found_related_products_df.sort_values(by=['similarity'], ascending=True)

        min_price_per, max_price_per = price_difference_range
        min_price = product_resource.product_price * min_price_per
        max_price = product_resource.product_price * max_price_per

        mask = (found_related_products_df['price'] > min_price) & (found_related_products_df['price'] < max_price)
        found_related_products_df = found_related_products_df[mask]

        if found_related_products_df.empty:
            return None

        found_related_products_df = found_related_products_df.head(1)

        found_related_products_df = found_related_products_df.drop(columns=['similarity'], axis=1)

        related_products = Utility.dataframe_to_dataclass(found_related_products_df, SerpResponseModel)

        return related_products[0]

