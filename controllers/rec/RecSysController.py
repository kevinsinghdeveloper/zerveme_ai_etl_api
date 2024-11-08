from dataclasses import asdict
from typing import cast

from flask import Flask, request, jsonify

from abstractions.IController import IController
from abstractions.IResourceManager import IResourceManager
from managers.rec.RecSysResourceManager import RecSysResourceManager
from models.request.RecRequestResourceModel import RecRequestResourceModel
from utility.Utility import Utility


class RecSysController(IController):
    def __init__(self, app: Flask, resource_manager: RecSysResourceManager):
        super().__init__(app, resource_manager)

    def register_all_routes(self):
        self.register_route("/related_products",
                            "get_related_products",
                            self.get_related_products,
                            "GET")

    def get_related_products(self):
        request_model = RecRequestResourceModel(
            product_title=request.args["product_name"],
            web_site=request.args["web_site"],
            product_price=Utility.clean_and_convert(request.args.get("price", 0))
        )

        data_response = self._resource_manager.get(request_model)

        return data_response

