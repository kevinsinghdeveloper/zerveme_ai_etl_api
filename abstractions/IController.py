from flask import Flask

from abstractions.IResourceManager import IResourceManager


class IController:
    def __init__(self, app: Flask, resource_manager: IResourceManager):
        self.__app = app
        self.__resource_manager = resource_manager

