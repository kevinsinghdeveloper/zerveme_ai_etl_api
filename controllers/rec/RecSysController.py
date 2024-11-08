from typing import cast

from flask import Flask, request

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
        # TODO add data class for response and request -> I think parameter is too generic
        request_model = RecRequestResourceModel(
            product_name=request.args["product_name"]
        )

        res_mng = self.get_resource_manager()
        res_mng.get(request_model) # we can probably still pass in a model resource_model -> we can define
        print("test", request.args) # we can extract the fields here and store in a model
        pass

