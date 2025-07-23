# TODO -> read config for serp api
from abc import abstractmethod
from typing import List, Union
from abstractions.models import ResponseModel, ParameterModel
from abstractions.models.RequestResourceModel import RequestResourceModel


class ILLMServiceManager:
    def __init__(self, config: dict):
        self._config = config

    @abstractmethod
    def submit_prompt(self, request_resource_model: RequestResourceModel) -> Union[List[ResponseModel] | None]:
        pass


    # def configure_llm(self):
    #     config = self.get_config()
    #     api_key = config["api_key"]
    #
    #     self.__model = OpenAI(api_key=api_key)
    #     self.__genai_config = config['gen_config']
    #     self.__model_name = config['model_name']


    # tokens etc?