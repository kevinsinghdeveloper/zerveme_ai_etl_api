from dataclasses import asdict
from typing import cast

from flask import Flask, request, jsonify

from abstractions.IController import IController
from abstractions.IResourceManager import IResourceManager
from managers.reports_processor.ReportProcessorResourceManager import ReportProcessorResourceManager
from models.request.ReportProcessorRequestResourceModel import ReportProcessorRequestResourceModel
from utility.Utility import Utility

'''
request.args -> query parameters
request.json -> body parameters
'''


class ReportProcessorController(IController):
    def get_resource_manager(self):
        pass

    def __init__(self, app: Flask, resource_manager: ReportProcessorResourceManager):
        super().__init__(app, resource_manager)

    def register_all_routes(self):
        self.register_route("/report_processor/get_job_status",
                            "get_job_status",
                            self.get_job_status,
                            "GET")
        self.register_route("/report_processor/start_job",
                            "start_job",
                            self.start_job,
                            "POST")
        self.register_route("/report_processor/stop_job",
                            "stop_job",
                            self.stop_job,
                            "POST")
    def get_job_status(self):
        request_model = ReportProcessorRequestResourceModel(
            task_type=request.json.get("task_type"),  # Changed from request.args to request.json
            task_params=request.json.get("task_params")  # Changed from request.args to request.json
        )
        data_response = self._resource_manager.get(request_model)
        return data_response

    def start_job(self):
        request_model = ReportProcessorRequestResourceModel(
            task_type=request.json.get("task_type"),
            task_params=request.json.get("task_params")
        )
        data_response = self._resource_manager.post(request_model)
        return data_response

    def stop_job(self):
        request_model = ReportProcessorRequestResourceModel(
            task_type=request.json.get("task_type"),
            task_params=request.json.get("task_params")
        )
        data_response = self._resource_manager.post(request_model)
        return data_response