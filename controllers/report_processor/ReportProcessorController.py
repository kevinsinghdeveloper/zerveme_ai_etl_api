from dataclasses import asdict
from typing import cast

from flask import Flask, request, jsonify

from abstractions.IController import IController
from abstractions.IResourceManager import IResourceManager
from managers.reports_processor.ReportProcessorResourceManager import ReportProcessorResourceManager
from models.request.ReportProcessorRequestResourceModel import ReportProcessorRequestResourceModel
from utility.Utility import Utility


class ReportProcessorController(IController):
    def __init__(self, app: Flask, resource_manager: ReportProcessorRequestResourceModel):
        super().__init__(app, resource_manager)

    def register_all_routes(self):
        # self.register_route("/report_processor",
        #                     "get_related_products",
        #                     self.get_related_products,
        #                     "GET")
        pass
    # def get_related_products(self):
    #     request_model = RecRequestResourceModel(
    #         product_title=request.args["product_name"],
    #         web_site=request.args["web_site"],
    #         product_price=Utility.clean_and_convert(request.args.get("price", 0))
    #     )
    #
    #     data_response = self._resource_manager.get(request_model)
    #
    #     return data_response

