from flask import Flask

from abstractions.IController import IController
from managers.auth.AuthenticationResourceManager import AuthenticationResourceManager


class AuthenticationController(IController):
    def get_resource_manager(self):
        pass

    def __init__(self, app: Flask, resource_manager: AuthenticationResourceManager):
        super().__init__(app, resource_manager)

    def register_all_routes(self):
        self.register_route(
            "/authentication",
            "authentication",
            self.authentication,
            "GET"
        )
        pass

    def authentication(self):
        pass

