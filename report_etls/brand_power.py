import json
import logging
from abstractions.EtlReportBase import EtlReportBase
from abstractions.ILLMServiceManager import ILLMServiceManager
from utility.Utility import Utility


class BrandPower(EtlReportBase):
    EXPECTED_RUN_PARAMS_FIELDS = [
        "target_industries",
        "company_name",
        "description_of_company",
        "company_website",
        "online_store",
        "location",
        "known_competitors"
    ]

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
        """
        Validates the run parameters for the Brand Power report.
        Ensures all required fields are present and correctly formatted.
        """
        missing_fields = set(self.EXPECTED_RUN_PARAMS_FIELDS) - set(self._run_params.keys())

        if missing_fields:
            raise ValueError(f"Missing required run parameters: {', '.join(missing_fields)}")

        # Check if target industries are valid
        target_industries = self._run_params.get("target_industries", [])

        if not target_industries:
            raise ValueError("Target industries cannot be empty.")

        if not all(industry in self.__industries for industry in target_industries):
            raise ValueError("Invalid target industries specified.")

        logging.info("Run parameters validated successfully.")