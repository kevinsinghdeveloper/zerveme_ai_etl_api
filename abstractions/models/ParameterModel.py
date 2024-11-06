from dataclasses import dataclass
from typing import Optional


@dataclass
class ParameterModel:
    id: Optional[int]
    body: dict
    # do we need header?
