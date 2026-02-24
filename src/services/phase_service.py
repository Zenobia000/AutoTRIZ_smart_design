"""Project state machine: DRAFT → PHASE_I → PHASE_II → PHASE_III → COMPLETED"""

VALID_TRANSITIONS = {
    "DRAFT": ["PHASE_I"],
    "PHASE_I": ["PHASE_II"],
    "PHASE_II": ["PHASE_III"],
    "PHASE_III": ["COMPLETED"],
    "COMPLETED": [],
}


def can_transition(current: str, target: str) -> bool:
    return target in VALID_TRANSITIONS.get(current, [])
