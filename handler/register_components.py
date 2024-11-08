from flask import Flask

from abstractions.IController import IController
from abstractions.IResourceManager import IResourceManager


def register_controller(app: Flask, controller: type[IController], resource_manager: IResourceManager):
    # Initialize the controller with its resource manager
    controller_instance = controller(app, resource_manager)

    # Register all routes of the controller
    controller_instance.register_all_routes()

    print(f"Registered controller: {controller.__name__}")