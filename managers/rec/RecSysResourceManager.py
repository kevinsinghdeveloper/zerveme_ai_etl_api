from dataclasses import asdict

from flask import jsonify

from abstractions.IWebServiceManager import IWebServiceManager
from abstractions.IResourceManager import IResourceManager
from managers.RecommendationEngineManager import RecommendationEngineManager

from models.request.RecRequestResourceModel import RecRequestResourceModel


class RecSysResourceManager(IResourceManager):
    def __init__(self, serp_service_manager: IWebServiceManager):
        super().__init__(serp_service_manager)

        self.__rec_eng_mngr = RecommendationEngineManager()

    def get(self, request_resource_model: RecRequestResourceModel):
        serp_data_items = self._web_service_manager.get(request_resource_model)

        best_items = []
        same_product_lower_price = self.__rec_eng_mngr.find_same_product(
            source_product_name=request_resource_model.product_title,
            related_products=serp_data_items,
            price_difference_range=None  #default to just finding any at lower (use lowest)
        )
        if same_product_lower_price:
            best_items.append(same_product_lower_price)

        related_product_tier_1 = self.__rec_eng_mngr.find_related_product(
            source_product_name=request_resource_model.product_title,
            related_products=serp_data_items,
            price_difference_range=(.2, .35)
        )
        if related_product_tier_1:
            best_items.append(related_product_tier_1)

        related_product_tier_2 = self.__rec_eng_mngr.find_related_product(
            source_product_name=request_resource_model.product_title,
            related_products=serp_data_items,
            price_difference_range=(.35, .5)  # default to just finding any at lower (use lowest)
        )
        if related_product_tier_2:
            best_items.append(related_product_tier_2)

        if len(best_items) == 0:
            best_items = serp_data_items[:3] # default top three for now

        return jsonify({"message": "Recommendation generated", "data": [asdict(d) for d in best_items]})
