import json
import logging
import os
from abc import abstractmethod, ABC

from abstractions.ILLMServiceManager import ILLMServiceManager


def run_pipeline(pipeline_tasks: dict):
    for name, task in pipeline_tasks.items():
        logging.info(f"Running task {name}...")
        task()
        logging.info(f"Task {name} completed successfully.")


class EtlReportBase(ABC):
    def __init__(self, run_params: dict, etl_name: str,
                 llm_service_manager: ILLMServiceManager):
        self._run_params = run_params
        self._llm_service_manager = llm_service_manager

        self._etl_name = etl_name
        self._pre_validation_pipeline_tasks = {}
        self._extract_pipeline_tasks = {}
        self._transform_process_pipeline_tasks = {}
        self._post_validation_pipeline_tasks = {}
        
        # Initialize caching
        self._llm_response_data = {}
        self._use_cache = run_params.get('use_cache', True)
        self._cache_file = f"cache/{etl_name}.json"

    def run_etl(self):
        logging.info(f"Running competitor tracking ETL process with "
                     f"config: {self._run_params}")

        self.configure_init_tasks()
        self.run_pre_validation()
        self.run_extract_tasks()
        self.run_transform_process_tasks()
        self.run_post_validation()

        # TODO update
        return {"status": "success",
                "message": "Competitor tracking completed."}

    def run_pre_validation(self):
        run_pipeline(self._pre_validation_pipeline_tasks)

    def run_post_validation(self):
        run_pipeline(self._post_validation_pipeline_tasks)

    def run_extract_tasks(self):
        run_pipeline(self._extract_pipeline_tasks)

    def run_transform_process_tasks(self):
        run_pipeline(self._transform_process_pipeline_tasks)

    def _json_serializer(self, obj):
        """Custom JSON serializer for objects that have to_dict method"""
        if hasattr(obj, 'to_dict') and callable(getattr(obj, 'to_dict')):
            return obj.to_dict()
        return str(obj)

    def save_cache(self):
        """Save LLM response data to cache file for debugging and testing"""
        if not self._use_cache:
            return
        os.makedirs(os.path.dirname(self._cache_file), exist_ok=True)
        with open(self._cache_file, 'w') as f:
            json.dump(self._llm_response_data, f, indent=2, default=self._json_serializer)
        logging.info(f"Cache saved to {self._cache_file}")

    def load_cache(self):
        """Load cached LLM response data if available and use_cache is True"""
        if self._use_cache and os.path.exists(self._cache_file):
            with open(self._cache_file, 'r') as f:
                self._llm_response_data = json.load(f)
            logging.info(f"Cache loaded from {self._cache_file}")
            return True
        return False

    def is_cached(self, key: str) -> bool:
        """Check if a specific key is already cached and use_cache is True"""
        return self._use_cache and key in self._llm_response_data


    @abstractmethod
    def configure_init_tasks(self):
        pass
