from enum import Enum
from typing import Any
from pydantic import BaseModel


class ConsequenceDecision(str, Enum):
    CONTINUE = "CONTINUE"
    PAUSE = "PAUSE"
    REBOUND = "REBOUND"
    REFUSE = "REFUSE"
    HALT = "HALT"


class ConsequenceRequest(BaseModel):
    motion_id: str
    actor_id: str
    authority_valid: bool = True
    evidence_fresh: bool = True
    integrity_ok: bool = True
    current_state_stable: bool = True
    energy: float = 10.0
    burden: float = 1.0
    debt: float = 0.0
    risk: float = 1.0
    concurrency: float = 1.0
    min_capacity: float = 1.0
    max_debt: float = 100.0
    protected_effect: str = "none"


class ConsequenceResponse(BaseModel):
    decision: ConsequenceDecision
    admissible: bool
    effect_allowed: bool
    reason: str
    capacity_phi: float
    projected_debt: float
    projected_burden: float
    receipt_hash: str
    record: dict[str, Any]
