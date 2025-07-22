import logging

from abstractions.EtlReportBase import EtlReportBase


class CompetitorTracker(EtlReportBase):
    def __init__(self, run_params: dict):
        super().__init__(run_params, "competitor_tracker")

    def configure_init_tasks(self):
        self._pre_validation_pipeline_tasks  = {
            "Check run params": self.__check_run_params
        }
    def __check_run_params(self):
        pass
