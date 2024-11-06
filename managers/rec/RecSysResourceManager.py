from typing import Union, List

from abstractions.IWebServiceManager import IWebServiceManager
from abstractions.IResourceManager import IResourceManager

from abstractions.models import EntityResource, ParameterModel


class RecSysResourceManager(IResourceManager):
    def __init__(self, web_service_manager: IWebServiceManager):
        super().__init__(web_service_manager)

    def create(self) -> EntityResource:  # we need an entity base model -> return id?
        pass

    def update(self, resource_id: int, entity_data: EntityResource):  # we need to define a base model to update with
        pass

    def get(self, resource_id: int) -> Union[List[EntityResource] | None]:  # return resource
        pass

    def get_data(self, parameters: ParameterModel) -> Union[
        List[EntityResource] | None]:  # get some data based on parameters
        pass
