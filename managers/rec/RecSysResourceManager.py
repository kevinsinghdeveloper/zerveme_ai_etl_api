from dataclasses import asdict

from flask import jsonify

from abstractions.IWebServiceManager import IWebServiceManager
from abstractions.IResourceManager import IResourceManager
from managers.RecommendationEngineManager import RecommendationEngineManager

from models.request.RecRequestResourceModel import RecRequestResourceModel


class RecSysResourceManager(IResourceManager):
    def __init__(self, serp_service_manager: IWebServiceManager, **kwargs):
        super().__init__(web_service_manager=serp_service_manager)

        config = kwargs.get('ml_config', None)
        if config is None:
            raise ValueError("Missing 'ml_config' in kwargs for RecommendationEngineManager")

        self.__rec_eng_mngr = RecommendationEngineManager(config)

    def get(self, request_resource_model: RecRequestResourceModel):
        serp_data_items = self._web_service_manager.get(request_resource_model)

        related_request_resource_model = request_resource_model
        related_request_resource_model.product_title = \
            f"Alternative products to `{related_request_resource_model.product_title}`"

        related_serp_data_items = self._web_service_manager.get(related_request_resource_model)

        best_items = {}
        same_product_lower_price = self.__rec_eng_mngr.find_same_product(
            product_resource=request_resource_model,
            related_product_name_field="product_title",
            related_products=serp_data_items,
            price_difference_range=None  #default to just finding any at lower (use lowest)
        )
        if same_product_lower_price:
            best_items['same_product'] = same_product_lower_price

        related_product_tier_1 = self.__rec_eng_mngr.find_related_product(
            product_resource=request_resource_model,
            related_products=related_serp_data_items,
            related_product_name_field="product_title",
            price_difference_range=(.35, .55)
        )
        if related_product_tier_1:
            best_items['related_1'] = related_product_tier_1

        related_product_tier_2 = self.__rec_eng_mngr.find_related_product(
            product_resource=request_resource_model,
            related_products=related_serp_data_items,
            related_product_name_field="product_title",
            price_difference_range=(.56, .75)  # default to just finding any at lower (use lowest)
        )
        if related_product_tier_2:
            best_items['related_2'] = related_product_tier_2

        results = {}
        if len(best_items) > 0:
            for d, item in best_items.items():
                results[d] = asdict(item)

        return jsonify({"message": "Recommendation generated", "data": [results]})
