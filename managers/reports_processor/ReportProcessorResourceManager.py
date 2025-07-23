from dataclasses import asdict
from typing import Optional, Dict, Union

from flask import jsonify

from abstractions.IServiceManagerBase import IServiceManagerBase
from abstractions.IWebServiceManager import IWebServiceManager
from abstractions.IResourceManager import IResourceManager
from managers.ai.AIServiceHandler import AIServiceHandler
from models.request.ReportProcessorRequestResourceModel import ReportProcessorRequestResourceModel


class ReportProcessorResourceManager(IResourceManager):
    def __init__(self, web_service_managers: Optional[Dict[str, IServiceManagerBase]] = None, **kwargs):
        super().__init__(web_service_manager=web_service_managers)
        self.__etl_service_manager = web_service_managers.get("etl_service_manager")

    def get(self, request_resource_model: ReportProcessorRequestResourceModel):

        # response = self.__etl_service_manager.run_task(request_resource_model)

        return jsonify({"message": "Getting status", "data": []})

    def post(self, request_resource_model: ReportProcessorRequestResourceModel):
        # TODO based on the request get the corresponding AI service manager

        ai_service_manager = AIServiceHandler.get_ai_service(request_resource_model.llm_config)
        self.__etl_service_manager.configure(ai_service_manager=ai_service_manager)

        response = self.__etl_service_manager.run_task(request_resource_model)
        return jsonify({"message": "Post request on task", "data": []})
        # return jsonify({"message": "Recommendation generated", "data": [results]})
