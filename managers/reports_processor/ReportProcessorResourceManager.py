from dataclasses import asdict
from typing import Optional, Dict

from flask import jsonify

from abstractions.IWebServiceManager import IWebServiceManager
from abstractions.IResourceManager import IResourceManager
from models.request.ReportProcessorRequestResourceModel import ReportProcessorRequestResourceModel


class ReportProcessorResourceManager(IResourceManager):
    def __init__(self, web_service_managers: Optional[Dict[str, IWebServiceManager]] = None, **kwargs):
        super().__init__(web_service_manager=web_service_managers)

    def get(self, request_resource_model: ReportProcessorRequestResourceModel):
        return jsonify({"message": "Getting status", "data": []})

    def post(self, request_resource_model: ReportProcessorRequestResourceModel):
        return jsonify({"message": "Post request on task", "data": []})
        # return jsonify({"message": "Recommendation generated", "data": [results]})
