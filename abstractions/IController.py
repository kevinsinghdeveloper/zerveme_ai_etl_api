from flask import Flask


class IController:
    def __init__(self, app: Flask):
        self.__app = app

