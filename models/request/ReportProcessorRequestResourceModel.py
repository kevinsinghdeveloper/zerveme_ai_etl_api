from dataclasses import dataclass
from typing import Optional

from abstractions.models.RequestResourceModel import RequestResourceModel


@dataclass
class ReportProcessorRequestResourceModel(RequestResourceModel):
    task_type: str # Start, Stop, Status
    task_params: dict # Parameters for the task, e.g., report ID, filters, etc.
    llm_config: dict
    # task_id: Optional[str] = None  # Unique identifier for the task, if applicable