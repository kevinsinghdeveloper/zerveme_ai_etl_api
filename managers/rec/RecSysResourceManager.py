from abstractions.IWebServiceManager import IWebServiceManager
from abstractions.IResourceManager import IResourceManager

from models.request.RecRequestResourceModel import RecRequestResourceModel


class RecSysResourceManager(IResourceManager):
    def __init__(self, serp_service_manager: IWebServiceManager):
        super().__init__(serp_service_manager)

    def get(self, request_resource_model: RecRequestResourceModel):
        print("I am here")
        pass
