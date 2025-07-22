import inspect

from abstractions.EtlReportBase import EtlReportBase
from abstractions.IETLServiceManager import IETLServiceManager
import os
import importlib.util

from models.request.ReportProcessorRequestResourceModel import ReportProcessorRequestResourceModel


class ReportJobTaskManager(IETLServiceManager):
    def __init__(self, etl_config: dict):
        super().__init__(etl_config)

    def __get_all_report_jobs(self):
        """
        Returns a dictionary of all available report jobs from the report_etls directory.
        Returns:
            dict: A dictionary containing report job information
        """
        reports = {}
        report_dir = "report_etls"  # Directory containing report job files
        
        # Check if directory exists
        if not os.path.exists(report_dir):
            return reports
            
        # Get all Python files in the report_etls directory
        for file in os.listdir(report_dir):
            if file.endswith(".py") and not file.startswith("__"):
                # Get the module name without .py extension
                module_name = os.path.splitext(file)[0]
                
                try:
                    # Create the full path to the file
                    file_path = os.path.join(report_dir, file)
                    
                    # Load the module dynamically
                    spec = importlib.util.spec_from_file_location(module_name, file_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Add to reports dictionary
                    # Using module name as key and module itself as value
                    reports[module_name] = module
                    
                except Exception as e:
                    print(f"Error loading report job {module_name}: {str(e)}")
        
        return reports

    def __get_report_instance(self, report_name: str, etl_config: dict) -> EtlReportBase | None:
        """
        Given a report name and config, returns an instance of the ETL class that inherits from ETLBase.

        Args:
            report_name (str): The name of the report (i.e., module name without .py).
            etl_config (dict): The configuration to pass into the ETL class constructor.

        Returns:
            ETLBase | None: An instantiated ETL class, or None if not found.
        """
        reports = self.__get_all_report_jobs()
        module = reports.get(report_name)

        if not module:
            print(f"Report module '{report_name}' not found.")
            return None

        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if inspect.isclass(attr) and issubclass(attr, EtlReportBase) and attr is not EtlReportBase:
                return attr(etl_config)

        print(f"No ETLBase subclass found in module '{report_name}'.")
        return None

    def run_task(self, request: ReportProcessorRequestResourceModel):
        etl_report = self.__get_report_instance("competitor_tracker", self._etl_config)

        if etl_report:
            etl_report.run_etl()
        else:
            raise Exception("Failed to create ETL report instance.")

        return {"status": "success", "message": "Report run completed."}

'''
0. Read in dict of all availabable report jobs -- Reports will be managed with this ETL service -- so IDs will need to be mapped here -- db reference the python file?
1. Will be fed job parameters from the .NET worker
2. Locate job configuration
3. Trigger the job ETL service

'''

'''
Jobs

1. We will have to store reports as code
2. We will have a json which points to the config code? Maybe like a mapping? -- 
3. Annoying to maintain since .NET references a report and the ETL references a report in a different location [SOLVE] db reference the python file?????

'''