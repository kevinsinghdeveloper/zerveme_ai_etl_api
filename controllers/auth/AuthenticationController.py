from dataclasses import asdict
from typing import cast

from flask import Flask, request, jsonify

from abstractions.IController import IController
from managers.auth.AuthenticationResourceManager import AuthenticationResourceManager
from managers.rec.RecSysResourceManager import RecSysResourceManager


class AuthenticationController(IController):
    def get_resource_manager(self):
        pass

    def __init__(self, app: Flask, resource_manager: AuthenticationResourceManager):
        super().__init__(app, resource_manager)

    def register_all_routes(self):
        self.register_route("/authentication",
                            "authentication",
                            self.authentication,
                            "GET")
        pass
    #def get_resource_manager(self):
    #    return cast(AuthenticationResourceManager, self._resource_manager)

    def authentication(self):
        pass

