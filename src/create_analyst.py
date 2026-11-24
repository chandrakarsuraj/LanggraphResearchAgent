
from src.utils.nodes import create_analyst, human_feedback
from langgraph.graph import StateGraph, START, END
from src.utils.state import GenerateAnalystSate
from src.utils.edges import should_continue


builder = StateGraph(GenerateAnalystSate)
builder.add_node("create_analyst", create_analyst)
builder.add_node("human_feedback", human_feedback)

builder.add_edge(START, "create_analyst")

builder.add_edge("create_analyst", "human_feedback")
builder.add_conditional_edges("human_feedback", should_continue)


graph = builder.compile()