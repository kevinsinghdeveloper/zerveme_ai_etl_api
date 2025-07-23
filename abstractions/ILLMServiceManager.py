# TODO -> read config for serp api
from abc import abstractmethod
from typing import List, Union

from abstractions.IServiceManagerBase import IServiceManagerBase
from abstractions.models import ResponseModel, ParameterModel
from abstractions.models.RequestResourceModel import RequestResourceModel


class ILLMServiceManager(IServiceManagerBase):
    def __init__(self, config: dict):
        super().__init__(config)

    @abstractmethod
    def run_task(self, request_resource_model: RequestResourceModel):
        pass

    @abstractmethod
    def get_base_prompt(self, prompt, llm_instructions):
        pass


    # def configure_llm(self):
    #     config = self.get_config()
    #     api_key = config["api_key"]
    #
    #     self.__model = OpenAI(api_key=api_key)
    #     self.__genai_config = config['gen_config']
    #     self.__model_name = config['model_name']


    # tokens etc?