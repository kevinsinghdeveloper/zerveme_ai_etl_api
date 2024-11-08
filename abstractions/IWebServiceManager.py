# TODO -> read config for serp api
from abc import abstractmethod
from typing import List, Union
from abstractions.models import ResponseModel, ParameterModel
from abstractions.models.RequestResourceModel import RequestResourceModel


class IWebServiceManager:
    def __init__(self, api_config: dict):
        self._api_config = api_config

        self.__params = self._api_config["api_filters"]

    def get_base_params(self) -> dict:
        return self.__params.copy()

    @abstractmethod
    def get(self, request_resource_model: RequestResourceModel) -> Union[List[ResponseModel] | None]:
        pass

    @abstractmethod
    def put(self, parameter: ParameterModel):
        pass


    # tokens etc?