import inspect
from typing import Union, List

from abstractions.EtlReportBase import EtlReportBase
from abstractions.IETLServiceManager import IETLServiceManager
import os
import importlib.util

from abstractions.ILLMServiceManager import ILLMServiceManager
from abstractions.models import ResponseModel
from abstractions.models.RequestResourceModel import RequestResourceModel
from models.request.LLMRequestResourceModel import LLMRequestResourceModel
from models.request.ReportProcessorRequestResourceModel import ReportProcessorRequestResourceModel
from models.response.LLMResponseModel import LLMResponseModel


class OpenAIServiceManager(ILLMServiceManager):
    def __init__(self, config: dict):
        super().__init__(config)

    def submit_prompt(self, request_resource_model: LLMRequestResourceModel) -> Union[List[LLMResponseModel] | None]:
        pass
