# TODO -> read config for serp api
from abstractions.IServiceManagerBase import IServiceManagerBase
from abstractions.models.RequestResourceModel import RequestResourceModel
from abstractions.models import ResponseModel


class IETLServiceManager(IServiceManagerBase):
    def configure(self, **kwargs) -> None:
        pass

    def __init__(self, config: dict):
        super().__init__(config)

    def run_task(self,
                 request_resource_model: RequestResourceModel
                 ) -> ResponseModel:
        pass

    # tokens etc?
