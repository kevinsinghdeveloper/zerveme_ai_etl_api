# TODO -> read config for serp api
from abc import abstractmethod
from typing import List, Union
from abstractions.models import ResponseModel, ParameterModel
from abstractions.models.RequestResourceModel import RequestResourceModel


class IServiceManagerBase:
    def __init__(self, config: dict):
        self._config = config


    @abstractmethod
    def configure(self, **kwargs) -> None:
        pass

    @abstractmethod
    def run_task(self, request: RequestResourceModel):
        pass

    # tokens etc?