import logging
from abc import abstractmethod

from abstractions.ILLMServiceManager import ILLMServiceManager


class EtlReportBase:
    def __init__(self, run_params: dict, etl_name: str, llm_service_manager: ILLMServiceManager):
        self._run_params = run_params
        self._llm_service_manager = llm_service_manager

        self._etl_name = etl_name
        self._pre_validation_pipeline_tasks = {}
        self._extract_pipeline_tasks = {}
        self._transform_process_pipeline_tasks = {}
        self._post_validation_pipeline_tasks = {}

    def run_etl(self):
        logging.info(f"Running competitor tracking ETL process with config: {self._run_params}")

        self.configure_init_tasks()
        self.run_pre_validation()
        self.run_extract_tasks()
        self.run_transform_process_tasks()
        self.run_post_validation()

        return {"status": "success", "message": "Competitor tracking completed."}

    def run_pipeline(self, pipeline_tasks: dict):
        for name, task in pipeline_tasks.items():
            logging.info(f"Running task {name}...")
            task()
            logging.info(f"Task {name} completed successfully.")

    def run_pre_validation(self):
        self.run_pipeline(self._pre_validation_pipeline_tasks)

    def run_post_validation(self):
        self.run_pipeline(self._post_validation_pipeline_tasks)

    def run_extract_tasks(self):
        self.run_pipeline(self._extract_pipeline_tasks)

    def run_transform_process_tasks(self):
        self.run_pipeline(self._transform_process_pipeline_tasks)

    @abstractmethod
    def configure_init_tasks(self):
        pass
