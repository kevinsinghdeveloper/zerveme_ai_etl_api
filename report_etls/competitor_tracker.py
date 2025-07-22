import logging

from abstractions.EtlReportBase import EtlReportBase


class CompetitorTracker(EtlReportBase):
    def __init__(self, run_params: dict):
        super().__init__(run_params)
        self.__pre_validation_pipeline_tasks = {}

    def run_etl(self):
        logging.info(f"Running competitor tracking ETL process with config: {self._run_params}")

        self.run_init_tasks()
        self.run_pre_validation()
        return {"status": "success", "message": "Competitor tracking completed."}

    def run_init_tasks(self):
        self.__pre_validation_pipeline_tasks  = {
            "Check run params": self.__check_run_params
        }

    def run_pre_validation(self):
        for name, task in self.__pre_validation_pipeline_tasks.items():
            logging.info(f"Running task {name}...")
            task()
            logging.info(f"Task {name} completed successfully.")

    def run_post_validation(self):
        pass

    def run_extract_tasks(self):
        pass

    def run_transform_process_tasks(self):
        pass
    def __check_run_params(self):
        pass
