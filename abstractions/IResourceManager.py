# TODO -> read config for serp api
from abc import abstractmethod
from typing import List, Union

from abstractions import IWebServiceManager
from abstractions.models import ResponseModel, ParameterModel, EntityResource


class IResourceManager:
    def __init__(self, web_service_manager: IWebServiceManager):
        self.__web_service_manager = web_service_manager

    @abstractmethod
    def create(self) -> EntityResource: # we need an entity base model -> return id?
        pass

    @abstractmethod
    def update(self, resource_id: int, entity_data: EntityResource): #we need to define a base model to update with
        pass

    @abstractmethod
    def get(self, resource_id: int) -> Union[List[EntityResource] | None]: # return resource
        pass

    @abstractmethod
    def get_data(self, parameters: ParameterModel) -> Union[List[EntityResource] | None]: # get some data based on parameters
        pass


    # tokens etc?