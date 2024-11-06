from typing import Union, List

from abstractions.IWebServiceManager import IWebServiceManager
from abstractions.models import ParameterModel, ResponseModel


class WebServiceManager(IWebServiceManager):
    def rest_get(self, parameter: ParameterModel) -> Union[List[ResponseModel] | None]:
        pass

    def rest_put(self, parameter: ParameterModel):
        pass

