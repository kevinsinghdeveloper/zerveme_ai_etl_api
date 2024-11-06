from typing import Union, List

from abstractions.IWebServiceManager import IWebServiceManager
from abstractions.models import ParameterModel, ResponseModel


class SerpServiceManager(IWebServiceManager):
    def get(self, parameter: ParameterModel) -> Union[List[ResponseModel] | None]:
        pass

    def put(self, parameter: ParameterModel):
        pass

