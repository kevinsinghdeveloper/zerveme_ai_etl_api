from dataclasses import dataclass
from typing import Optional


@dataclass
class ParameterModel:
    id: Optional[int]
    api_path: Optional[str]
    body: dict
    # do we need header?
