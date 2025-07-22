from dataclasses import asdict
from typing import Optional, Dict, Union

from flask import jsonify

from abstractions.IETLServiceManager import IETLServiceManager
from abstractions.IWebServiceManager import IWebServiceManager
from abstractions.IResourceManager import IResourceManager
from models.request.ReportProcessorRequestResourceModel import ReportProcessorRequestResourceModel


class ReportProcessorResourceManager(IResourceManager):
    def __init__(self, web_service_managers: Optional[Dict[str, Union[IWebServiceManager, IETLServiceManager]]] = None, **kwargs):
        super().__init__(web_service_manager=web_service_managers)
        self.__etl_service_manager = web_service_managers.get("etl_service_manager")


    def get(self, request_resource_model: ReportProcessorRequestResourceModel):

        # response = self.__etl_service_manager.run_task(request_resource_model)

        return jsonify({"message": "Getting status", "data": []})

    def post(self, request_resource_model: ReportProcessorRequestResourceModel):
        response = self.__etl_service_manager.run_task(request_resource_model)
        return jsonify({"message": "Post request on task", "data": []})
        # return jsonify({"message": "Recommendation generated", "data": [results]})
