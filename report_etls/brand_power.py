import json
import logging
from abstractions.EtlReportBase import EtlReportBase
from abstractions.ILLMServiceManager import ILLMServiceManager
from utility.Utility import Utility


class BrandPower(EtlReportBase):
    def __init__(self, run_params: dict, llm_service_manager: ILLMServiceManager):
        super().__init__(run_params, "brand_power", llm_service_manager)
        # run params should contain ai configuration
        self.__report_name = None
        self.__report_id = None

        self.__industries = (Utility
                             .read_in_json_file("report_etls/report_resources/brand_power_resources/industries.json"))

    def configure_init_tasks(self):
        self._pre_validation_pipeline_tasks  = {
            "Check run params": self.__check_run_params
        }
    def __check_run_params(self):
        pass