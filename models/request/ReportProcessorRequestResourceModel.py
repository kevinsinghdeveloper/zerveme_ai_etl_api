from dataclasses import dataclass
from typing import Optional

from abstractions.models.RequestResourceModel import RequestResourceModel


@dataclass
class ReportProcessorRequestResourceModel(RequestResourceModel):
    task_type: Optional[str] = None # Start, Stop, Status
    task_params: Optional[dict] = None  # Parameters for the task, e.g., report ID, filters, etc.
    # task_id: Optional[str] = None  # Unique identifier for the task, if applicable