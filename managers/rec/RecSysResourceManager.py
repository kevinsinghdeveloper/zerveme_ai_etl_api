from dataclasses import asdict

from flask import jsonify

from abstractions.IWebServiceManager import IWebServiceManager
from abstractions.IResourceManager import IResourceManager

from models.request.RecRequestResourceModel import RecRequestResourceModel


class RecSysResourceManager(IResourceManager):
    def __init__(self, serp_service_manager: IWebServiceManager):
        super().__init__(serp_service_manager)

    def get(self, request_resource_model: RecRequestResourceModel):
        serp_data_items = self._web_service_manager.get(request_resource_model)

        return jsonify({"message": "Recommendation generated", "data": [asdict(d) for d in serp_data_items]})
