from abc import abstractmethod


class EtlReportBase:
    def __init__(self, run_params: dict):
        self._run_params = run_params

    @abstractmethod
    def run_etl(self):
        pass

    @abstractmethod
    def run_init_tasks(self):
        pass

    @abstractmethod
    def run_pre_validation(self):
        pass

    @abstractmethod
    def run_post_validation(self):
        pass

    @abstractmethod
    def run_extract_tasks(self):
        pass

    @abstractmethod
    def run_transform_process_tasks(self):
        pass