# TODO -> read config for serp api
from abc import abstractmethod
from typing import List, Union
from abstractions.models import ResponseModel, ParameterModel


class IWebServiceManager:
    def __init__(self, api_config: dict):
        self.__api_config = api_config

    @abstractmethod
    def get(self, parameter: ParameterModel) -> Union[List[ResponseModel] | None]:
        pass

    @abstractmethod
    def put(self, parameter: ParameterModel):
        pass

    # tokens etc?