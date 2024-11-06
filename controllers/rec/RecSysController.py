from flask import Flask

from abstractions.IController import IController


class RecSysController(IController):
    def __init__(self, app: Flask):
        super().__init__(app)

    # TODO add calls -> do research

