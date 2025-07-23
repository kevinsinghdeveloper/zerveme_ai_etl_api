import json
import logging
from abstractions.EtlReportBase import EtlReportBase
from abstractions.ILLMServiceManager import ILLMServiceManager
from utility.Utility import Utility

FORMAT_INSTRUCTIONS = ("Please include traits describing each competitor using this mapping {industry_traits_mapping} "
                       "Please format the output as a JSON object with the following structure: "
                       "")

LIST_COMPETITORS_BASE_PROMPT = ("Please list top 10 competitors for the company` `{company_name}` and website `{company_website}` "
                                "in the `{industries}` industries, in location `{location}`. "
                                "Short description of this company is `{description}`."
                                "Known competitors are `{competitors}`.")
LIST_COMPETITORS_SYS_PROMPT = "You are an expert in market analysis and competitor identification." \

class BrandPower(EtlReportBase):
    EXPECTED_RUN_PARAMS_FIELDS = [
        "target_industries",
        "company_name",
        "description_of_company",
        "company_website",
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

        self.__top_industry_sources = (Utility
                                     .read_in_json_file("report_etls/report_resources/brand_power_resources/top_industry_sources.json"))

        self.__system_context_prompt = None

    def configure_init_tasks(self):
        self._pre_validation_pipeline_tasks  = {
            "Check run params": self.__check_run_params
        }
        self._extract_pipeline_tasks = {
            "Generate prompts": self.__craft_prompts
        }
    def __check_run_params(self):
        """
        Validates the run parameters for the Brand Power report.
        Ensures all required fields are present and correctly formatted.
        """
        missing_fields = set(self.EXPECTED_RUN_PARAMS_FIELDS) - set(self._run_params.keys())

        if missing_fields:
            raise ValueError(f"Missing required run parameters: {', '.join(missing_fields)}")

        # check if fields are not empty
        for field in self.EXPECTED_RUN_PARAMS_FIELDS:
            if not self._run_params.get(field):
                raise ValueError(f"Run parameter '{field}' cannot be empty.")

        # Check if target industries are valid
        target_industries = self._run_params.get("target_industries", [])

        if not target_industries:
            raise ValueError("Target industries cannot be empty.")

        if not all(industry.lower() in (i.lower() for i in self.__industries) for industry in target_industries):
            raise ValueError("Invalid target industries specified.")

        logging.info("Run parameters validated successfully.")

    def __get_list_competitors_prompt(self):
        """
        Generates the prompt for listing competitors based on the run parameters.
        """
        company_name = self._run_params.get("company_name")
        company_website = self._run_params.get("company_website")
        industries = self._run_params.get("target_industries")
        location = self._run_params.get("location")
        description = self._run_params.get("description_of_company", "")
        competitors = self._run_params.get("known_competitors", [])

        return LIST_COMPETITORS_BASE_PROMPT.format(
            company_name=company_name,
            company_website=company_website,
            industries=",".join(industries),
            location=location,
            description=description,
            competitors=",".join(competitors)
        )

    def __craft_prompts(self):
        logging.info("Crafting prompts.")

        list_competitors_prompt = self.__get_list_competitors_prompt()



        pass

