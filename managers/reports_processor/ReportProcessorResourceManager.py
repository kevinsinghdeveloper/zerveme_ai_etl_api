from flask import jsonify
from typing import Optional, Dict

from abstractions.IServiceManagerBase import IServiceManagerBase
from abstractions.IResourceManager import IResourceManager
from managers.ai.AIServiceHandler import AIServiceHandler
from models.request.ReportProcessorRequestResourceModel import ReportProcessorRequestResourceModel


class ReportProcessorResourceManager(IResourceManager):
    def __init__(self, web_service_managers: Optional[Dict[str, IServiceManagerBase]] = None, **kwargs):
        super().__init__(web_service_manager=web_service_managers)
        self.__etl_service_manager = web_service_managers.get("etl_service_manager")

    def get(self, request_resource_model: ReportProcessorRequestResourceModel):
        return jsonify({"message": "Getting status", "data": []})

    def post(self, request_resource_model: ReportProcessorRequestResourceModel):
        llm_manager = AIServiceHandler.get_ai_service(request_resource_model.llm_config)
        self.__etl_service_manager.configure(llm_manager=llm_manager)
        response = self.__etl_service_manager.run_task(request_resource_model)
        return jsonify({"message": "Post request on task", "data": []})
