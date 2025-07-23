import inspect
from typing import Union, List

from abstractions.EtlReportBase import EtlReportBase
from abstractions.IETLServiceManager import IETLServiceManager
import os
import importlib.util
from openai import OpenAI

from abstractions.ILLMServiceManager import ILLMServiceManager
from abstractions.models import ResponseModel
from abstractions.models.RequestResourceModel import RequestResourceModel
from models.request.LLMRequestResourceModel import LLMRequestResourceModel
from models.request.ReportProcessorRequestResourceModel import ReportProcessorRequestResourceModel
from models.response.LLMResponseModel import LLMResponseModel


class OpenAIServiceManager(ILLMServiceManager):
    def __init__(self, config: dict):
        super().__init__(config)
        self.__model_name = None
        self.__genai_config = None
        self.__model = None

    def configure(self, **kwargs) -> None:
        config = self._config
        api_key = config["api_key"]

        self.__model = OpenAI(api_key=api_key)
        self.__genai_config = config['gen_config']
        self.__model_name = config['model_name']

    def __process_and_extract_response(self, response):
        # single choice n == 1
        response_message = response.choices[0].message.content
        usage_data = response.usage

        return response_message, usage_data

    def get_base_prompt(self, prompt: str, llm_instructions: str):
        system_prompt = {"role": "system", "content": llm_instructions}
        base_prompt = {"role": "user", "content": prompt}

        return system_prompt, base_prompt

    def run_task(self, request_resource_model: LLMRequestResourceModel):
        system_prompt, base_prompt = self.get_base_prompt(request_resource_model.prompt,
                                                          request_resource_model.instructions_prompt)

        response = self.__model.chat.completions.create(
            model=self.__model_name,
            messages=[
                system_prompt, base_prompt
            ],
            response_format={"type": "json_object"},
            temperature=self.__genai_config.get("temperature", 1),
            max_tokens=self.__genai_config.get("max_output_tokens", 500)
        )

        cleaned_response, usage = self.__process_and_extract_response(response)

        return cleaned_response, usage
