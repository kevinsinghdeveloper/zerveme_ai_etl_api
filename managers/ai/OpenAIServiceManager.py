import inspect
import json
import logging
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
from models.request.LLMResponseResourceModel import LLMResponseResourceModel
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

    def run_task(self, request_resource_model: LLMRequestResourceModel) -> LLMResponseResourceModel:
        # Construct prompts
        system_prompt, base_prompt = self.get_base_prompt(
            request_resource_model.prompt,
            request_resource_model.system_prompt
        )

        # Prepare messages
        history_messages = request_resource_model.history_messages or []

        # Always prepend system prompt if not already included
        messages = [{"role": "system", "content": request_resource_model.system_prompt}] + history_messages
        if not any(m["role"] == "user" for m in history_messages):
            messages.append({"role": "user", "content": request_resource_model.prompt})

        # Determine response_type
        response_type = request_resource_model.response_type or "str"

        # Run the model
        response = self.__model.chat.completions.create(
            model=self.__model_name,
            messages=messages,
            response_format={"type": "json_object"},
            temperature=self.__genai_config.get("temperature", 1),
            max_tokens=self.__genai_config.get("max_output_tokens", 500)
        )

        # Extract response content + usage
        cleaned_response, usage = self.__process_and_extract_response(response)

        # Save updated message history
        new_history = messages + [{"role": "assistant", "content": cleaned_response}]

        # Convert to dict if needed
        if response_type == "dict":
            try:
                cleaned_response = json.loads(cleaned_response)
            except json.JSONDecodeError as e:
                logging.warning(f"Failed to parse response as JSON: {e}")
                raise ValueError("Invalid JSON returned by model.")

        # Build response model
        return LLMResponseResourceModel(
            response_content=cleaned_response,
            history_messages=new_history,
            usage_data=usage
        )
