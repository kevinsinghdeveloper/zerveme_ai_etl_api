# TODO -> read config for serp api
from abc import abstractmethod
from typing import List, Union
from abstractions.models import ResponseModel, ParameterModel
from abstractions.models.RequestResourceModel import RequestResourceModel


class IETLServiceManager:
    def __init__(self, etl_config: dict):
        self._etl_config = etl_config

    def run_task(self, request_resource_model: RequestResourceModel) -> ResponseModel:
        pass

    # tokens etc?