
from src.utils.nodes import create_analyst
from langgraph.graph import StateGraph, START, END
from src.utils.state import GenerateAnalystSate



builder = StateGraph(GenerateAnalystSate)
builder.add_node("create_analyst", create_analyst)

builder.add_edge(START, "create_analyst")
builder.add_edge("create_analyst", END)


graph = builder.compile()