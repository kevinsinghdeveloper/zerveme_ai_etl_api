# TODO -> read config for serp api
from abc import abstractmethod

from abstractions.IServiceManagerBase import IServiceManagerBase
from abstractions.models.RequestResourceModel import RequestResourceModel
from models.request.LLMResponseResourceModel import LLMResponseResourceModel


class ILLMServiceManager(IServiceManagerBase):
    def __init__(self, config: dict):
        super().__init__(config)

    @abstractmethod
    def run_task(self, request_resource_model: RequestResourceModel) -> LLMResponseResourceModel:
        pass

    @abstractmethod
    def get_base_prompt(self, prompt, llm_instructions):
        pass

    # tokens etc?