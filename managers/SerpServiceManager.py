from typing import Union, List

from abstractions.IWebServiceManager import IWebServiceManager
from abstractions.models import ParameterModel, ResponseModel

import requests
import json

from models.request.RecRequestResourceModel import RecRequestResourceModel
from models.response.SerpResponseModel import SerpResponseModel
from utility.Utility import Utility


class SerpServiceManager(IWebServiceManager):
    def __init(self, api_config: dict):
        super().__init__(api_config)

    def get(self, rec_resource_model: RecRequestResourceModel) -> Union[List[SerpResponseModel] | None]:
        product_title = rec_resource_model.product_title
        #web_site = rec_resource_model.web_site

        params = self.get_base_params()

        params['q'] = product_title

        api_result = None
        try:
            api_result = requests.get(self._api_config["api_base_url"], params)
            api_result.raise_for_status()  # Raise an HTTPError for bad responses (4xx, 5xx)
        except requests.exceptions.HTTPError as http_err:
            Utility.error_log(f"HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            Utility.error_log(f"Connection error occurred: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            Utility.error_log(f"Timeout error occurred: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            Utility.error_log(f"An error occurred: {req_err}")

        if api_result is None:
            Utility.error_log("Failed to get response from serp")
            return []

        api_result = api_result.json()

        related_shopping_items_key = self._api_config['result_config']["related_shopping_items"]
        nested_keys_to_use = self._api_config['result_config']["nested_keys_to_use"]

        related_shopping_items = api_result[related_shopping_items_key]

        if len(related_shopping_items) == 0:
            Utility.error_log("No results returned from serp")
            return []

        serp_response_items = []
        for item in related_shopping_items:
            serp_response = SerpResponseModel(
                product_title=item.get(nested_keys_to_use['product_title'], None),
                product_id=item.get(nested_keys_to_use['product_id'], None),
                url=item.get(nested_keys_to_use['url'], None),
                merchant=item.get(nested_keys_to_use['merchant'], None),
                price=Utility.clean_and_convert(item.get(nested_keys_to_use['price'], 0)),
                position_rank=Utility.clean_and_convert(item.get(nested_keys_to_use['position_rank'], 0)),
                rating=Utility.clean_and_convert(item.get(nested_keys_to_use['rating'], 0)),
                reviews=Utility.clean_and_convert(item.get(nested_keys_to_use['reviews'], 0)),
                product_image=item.get(nested_keys_to_use['product_image'], None),
            )

            serp_response_items.append(serp_response)

        return serp_response_items

    def put(self, parameter: ParameterModel):
        pass
