from typing import Union, List

from abstractions.IWebServiceManager import IWebServiceManager
from abstractions.models import ParameterModel, ResponseModel

import requests
import json


class SerpServiceManager(IWebServiceManager):
    def __init(self, api_config: dict):
        super().__init__(api_config)

    def get(self, parameter: ParameterModel) -> Union[List[ResponseModel] | None]:
        data = parameter["body"]

        params = self.get_base_params()

        api_result = requests.get(self.__api_config["api_base_url"], params).json()

        api_result = api_result.get("return_object_key", None)

        # parse through the api result and get related items

    def put(self, parameter: ParameterModel):
        pass



