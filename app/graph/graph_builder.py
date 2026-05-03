from langgraph.graph import StateGraph, END
from app.graph.state import ProcurementState
from app.graph.nodes import (
    check_inventory_node,
    procurement_node,
    approval_node,
    send_po_node,
    logistics_node
)
from app.graph.edges import should_procure


def build_graph(db):
    builder = StateGraph(ProcurementState)

    builder.add_node("check_inventory", lambda state: check_inventory_node(state, db))
    builder.add_node("procurement", lambda state: procurement_node(state, db))
    builder.add_node("approval", approval_node)
    builder.add_node("send_po", send_po_node)
    builder.add_node("logistics", logistics_node)

    builder.set_entry_point("check_inventory")

    # Conditional edge
    builder.add_conditional_edges(
        "check_inventory",
        should_procure,
        {
            "procure": "procurement",
            "end": END
        }
    )

    builder.add_edge("procurement", "approval")
    builder.add_edge("approval", "send_po")
    builder.add_edge("send_po", "logistics")
    builder.add_edge("logistics", END)

    return builder.compile()