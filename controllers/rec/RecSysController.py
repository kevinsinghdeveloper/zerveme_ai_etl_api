from dataclasses import asdict
from typing import cast

from flask import Flask, request, jsonify

from abstractions.IController import IController
from abstractions.IResourceManager import IResourceManager
from managers.rec.RecSysResourceManager import RecSysResourceManager
from models.request.RecRequestResourceModel import RecRequestResourceModel


class RecSysController(IController):
    def __init__(self, app: Flask, resource_manager: RecSysResourceManager):
        super().__init__(app, resource_manager)

    def register_all_routes(self):
        self.register_route("/related_products",
                            "get_related_products",
                            self.get_related_products,
                            "GET")

    def get_resource_manager(self):
        return cast(RecSysResourceManager, self._resource_manager)

    def get_related_products(self):
        request_model = RecRequestResourceModel(
            product_title=request.args["product_name"],
            #web_site=request.args["web_site"]
        )

        res_mng = self.get_resource_manager()
        data_response = res_mng.get(request_model)

        return data_response

