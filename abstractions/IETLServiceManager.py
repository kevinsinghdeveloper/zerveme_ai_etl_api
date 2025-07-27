# TODO -> read config for serp api
from abc import abstractmethod

from abstractions.IServiceManagerBase import IServiceManagerBase
from abstractions.models.RequestResourceModel import RequestResourceModel


class IETLServiceManager(IServiceManagerBase):
    def __init__(self, config: dict):
        super().__init__(config)

    def run_task(self, request_resource_model: RequestResourceModel):
        pass

    # tokens etc?