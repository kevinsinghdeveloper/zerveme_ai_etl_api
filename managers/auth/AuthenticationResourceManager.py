from abstractions.IResourceManager import IResourceManager
from models.request.AuthRequestResourceModel import AuthRequestResourceModel


class AuthenticationResourceManager(IResourceManager):
    def __init__(self):
        super().__init__()

    def get(self, auth_resource_model: AuthRequestResourceModel):
        # send key to get jwt token
        # hard code for now -> we will need a db to handle multiple keys
        return []
