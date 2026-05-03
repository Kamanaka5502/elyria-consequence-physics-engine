from app.models import ConsequenceDecision, ConsequenceRequest, ConsequenceResponse
from app.receipts import sha256


def resolve_consequence(req: ConsequenceRequest) -> ConsequenceResponse:
    projected_burden = float(req.burden) * float(req.risk) * float(req.concurrency)
    capacity_phi = float(req.energy) - projected_burden - float(req.min_capacity)
    projected_debt = float(req.debt) + projected_burden

    admissible = (
        req.authority_valid
        and req.evidence_fresh
        and req.integrity_ok
        and req.current_state_stable
        and capacity_phi >= 0
        and projected_debt <= req.max_debt
    )

    if not req.integrity_ok:
        decision = ConsequenceDecision.HALT
        reason = "integrity_failure"
    elif not req.current_state_stable:
        decision = ConsequenceDecision.REBOUND
        reason = "unstable_state_requires_rebound"
    elif not req.authority_valid:
        decision = ConsequenceDecision.REFUSE
        reason = "authority_invalid"
    elif not req.evidence_fresh:
        decision = ConsequenceDecision.PAUSE
        reason = "evidence_stale_requires_pause"
    elif capacity_phi < 0:
        decision = ConsequenceDecision.HALT
        reason = "capacity_collapse"
    elif projected_debt > req.max_debt:
        decision = ConsequenceDecision.REFUSE
        reason = "debt_boundary_exceeded"
    elif capacity_phi < (0.15 * max(req.energy, 1e-9)):
        decision = ConsequenceDecision.PAUSE
        reason = "near_boundary_capacity_pressure"
    else:
        decision = ConsequenceDecision.CONTINUE
        reason = "consequence_admissible"

    effect_allowed = decision == ConsequenceDecision.CONTINUE

    record = {
        "motion_id": req.motion_id,
        "actor_id": req.actor_id,
        "decision": decision.value,
        "effect_allowed": effect_allowed,
        "reason": reason,
        "capacity_phi": capacity_phi,
        "projected_burden": projected_burden,
        "projected_debt": projected_debt,
        "protected_effect": req.protected_effect,
    }
    receipt_hash = sha256({"request": req, "record": record})
    record["receipt_hash"] = receipt_hash

    return ConsequenceResponse(
        decision=decision,
        admissible=admissible,
        effect_allowed=effect_allowed,
        reason=reason,
        capacity_phi=capacity_phi,
        projected_debt=projected_debt,
        projected_burden=projected_burden,
        receipt_hash=receipt_hash,
        record=record,
    )
