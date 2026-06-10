from langgraph.graph import StateGraph, START, END

from app.agents.state import WorkoutState
from app.agents.memory_agent import memory_agent
from app.agents.rag_agent import rag_agent
from app.agents.planner_agent import planner_agent


def build_workout_graph():
    graph_builder = StateGraph(WorkoutState)

    graph_builder.add_node("memory", memory_agent)
    graph_builder.add_node("rag", rag_agent)
    graph_builder.add_node("planner", planner_agent)

    graph_builder.add_edge(START, "memory")
    graph_builder.add_edge("memory", "rag")
    graph_builder.add_edge("rag", "planner")
    graph_builder.add_edge("planner", END)

    return graph_builder.compile()


workout_graph = build_workout_graph()