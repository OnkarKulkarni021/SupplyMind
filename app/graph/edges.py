def should_procure(state):
    return "procure" if state["is_low"] else "end"


def approval_decision(state):
    return state["approval_status"]