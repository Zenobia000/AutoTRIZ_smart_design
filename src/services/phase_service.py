"""Project state machine: DRAFT → PHASE_1 → PHASE_2 → PHASE_3 → COMPLETED"""

VALID_TRANSITIONS = {
    "DRAFT": ["PHASE_1"],
    "PHASE_1": ["PHASE_2"],
    "PHASE_2": ["PHASE_3"],
    "PHASE_3": ["COMPLETED"],
    "COMPLETED": [],
}


def can_transition(current: str, target: str) -> bool:
    return target in VALID_TRANSITIONS.get(current, [])
