# TODO -> read config for serp api
from abc import abstractmethod
from typing import List, Union, Dict, Optional

from abstractions import IWebServiceManager
from abstractions.models.RequestResourceModel import RequestResourceModel
from abstractions.models.ResponseModel import ResponseModel


class IResourceManager:
    def __init__(self, web_service_manager: Optional[Dict[str, IWebServiceManager]] = None):
        self._web_service_managers = web_service_manager

    @abstractmethod
    def get(self, request_resource_model: RequestResourceModel) -> ResponseModel:
        pass
