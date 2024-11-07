from flask import Flask

from abstractions.IController import IController
from abstractions.IResourceManager import IResourceManager


class RecSysController(IController):
    def __init__(self, app: Flask, resource_manager: IResourceManager):
        super().__init__(app, resource_manager)

    def register_all_routes(self):
        self.register_route("/related_products",
                            "get_related_products",
                            self.get_related_products,
                            "GET")

    # TODO add calls -> do research
    # TODO look at old code on how related products are pulled


    def get_related_products(self):
        print("test")
        pass

