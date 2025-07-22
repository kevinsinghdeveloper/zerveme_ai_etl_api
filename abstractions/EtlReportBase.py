from abc import abstractmethod


class EtlReportBase:
    def __init__(self):
        pass

    @abstractmethod
    def run_etl(self):
        pass
