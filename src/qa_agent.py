
from src.utils.state import InterviewState
from src.utils.nodes import generate_question, search_web, search_web2, generate_answer, save_interview, write_section
from src.utils.edges import  route_messages
from langgraph.graph import StateGraph, START, END

# Add nodes and edges 
builder = StateGraph(InterviewState)
builder.add_node("ask_question", generate_question)
builder.add_node("search_web", search_web)
builder.add_node("search_web2", search_web2)
builder.add_node("answer_question", generate_answer)
builder.add_node("save_interview", save_interview)
builder.add_node("write_section", write_section)

# Flow
builder.add_edge(START, "ask_question")
builder.add_edge("ask_question", "search_web")
builder.add_edge("ask_question", "search_web2")
builder.add_edge("search_web", "answer_question")
builder.add_edge("search_web2", "answer_question")
builder.add_conditional_edges("answer_question", route_messages,['ask_question','save_interview'])
builder.add_edge("save_interview", "write_section")
builder.add_edge("write_section", END)

graph = builder.compile()