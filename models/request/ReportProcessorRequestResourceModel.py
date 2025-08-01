from dataclasses import dataclass

from abstractions.enumerations.JobStatusEnum import JobStatusEnum
from abstractions.models.RequestResourceModel import RequestResourceModel


@dataclass
class ReportProcessorRequestResourceModel(RequestResourceModel):
    task_type: JobStatusEnum
    report_name: str
    task_params: dict
    llm_config: dict
