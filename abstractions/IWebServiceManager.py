# TODO -> read config for serp api
from abc import abstractmethod
from typing import List, Union
from abstractions.models import ResponseModel, ParameterModel


class IWebServiceManager:
    def __init__(self, web_config):
        self.__web_config = web_config

    @abstractmethod
    def rest_get(self, parameter: ParameterModel) -> Union[List[ResponseModel] | None]:
        pass

    @abstractmethod
    def rest_put(self, parameter: ParameterModel):
        pass

    # tokens etc?