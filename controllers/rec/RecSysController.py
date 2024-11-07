from flask import Flask

from abstractions.IController import IController
from abstractions.IResourceManager import IResourceManager


class RecSysController(IController):
    def __init__(self, app: Flask, resource_manager: IResourceManager):
        super().__init__(app, resource_manager)

    # TODO add calls -> do research

