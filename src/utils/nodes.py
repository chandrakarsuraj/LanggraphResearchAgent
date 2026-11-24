

from dotenv import load_dotenv
from src.utils.state import GenerateAnalystSate, InterviewState, ResearchGraphState
from typing import Dict, Any
from src.utils.models import llm
from src.utils.objects import Perspective, SearchQuery
from src.utils.prompts import *
from langchain_core.messages import HumanMessage, AIMessage,SystemMessage
from langgraph.types import interrupt
from src.utils.objects import Analyst
from langchain_tavily import TavilySearch
from langchain_core.messages import get_buffer_string

load_dotenv()


# nodes

def create_analyst(state:GenerateAnalystSate)->Dict[str, Any]:
    """Create analyst"""
    topic = state["topic"]
    max_analyst = state["max_analysts"]
    human_analyst_feedback = state.get("human_analyst_feedback")

    # Enforce Structere Output
    structured_llm = llm.with_structured_output(Perspective)


    # System message
    
    messages = [
        SystemMessage( analyst_instructions),
        HumanMessage(f""" 
            Topic: {topic},
            Max Analyst : {max_analyst},
            Human analyst feedback: {human_analyst_feedback}
        """)
    ]

    res = structured_llm.invoke(messages)
    return {"analysts": res.analysts}



def human_feedback(state:GenerateAnalystSate)->Dict[str, Any]:
    """This is human feedback about the analyst given"""

    feedback = interrupt(
        {
            "question": "Are these analyst okay for you?",
            "analyst":[
               analyst.model_dump()  for analyst in state.get("analysts", [])
                
            ],
            "instructions": "Return feedback to regenerate analysts or return empty/perfect/continue/okay and continue the graph"
        }
    )
    if feedback is None:
        return {"human_analyst_feedback" : None}

    if feedback.lower() in {"perfect","okay", "yes", "continue" }:
        return {"human_analyst_feedback": None}

    return {"human_analyst_feedback": feedback}


def generate_question(state: InterviewState):
    """Node to generate questions"""
    
    
    analyst = state["analyst"]
    if isinstance(analyst, dict):
        analyst = Analyst.model_validate(analyst)


    messages = state["messages"]

    system_message = question_instructions.format(goals=analyst.persona)

    question = llm.invoke(

        [SystemMessage(system_message) ]+ messages
    )

    return {"messages": [question]}


def search_web(state: InterviewState):
    """Retrive docs from web"""

    structured_llm = llm.with_structured_output(SearchQuery)

    search_intstruction_system_message = SystemMessage(search_instructions)
    search_query = structured_llm.invoke([search_intstruction_system_message]+ state["messages"])
    response = TavilySearch(max_resulsts = 3).invoke({"query": search_query.search_query})
    search_docs =  response.get("results", [])


    # Format
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
            for doc in search_docs
        ]
    )

    return {"context": [formatted_search_docs]}


def search_web2(state: InterviewState):
    """Retrive docs from web"""

    structured_llm = llm.with_structured_output(SearchQuery)

    search_intstruction_system_message = SystemMessage(search_instructions)
    search_query = structured_llm.invoke([search_intstruction_system_message]+ state["messages"])
    response = TavilySearch(max_resulsts = 3).invoke({"query": search_query.search_query})
    search_docs =  response.get("results", [])


    # Format
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
            for doc in search_docs
        ]
    )

    return {"context": [formatted_search_docs]}



def generate_answer(state: InterviewState):
    """Node to answer questions"""

    analyst = state["analyst"]
    messages = state["messages"]
    context = state["context"]


    if isinstance(analyst, dict):
        analyst = Analyst.model_validate(analyst)

    system_message = answer_instructions.format(goals = analyst.persona, context=context)

    answer = llm.invoke([SystemMessage(system_message)]+messages)

    answer.name = "expert"

    return {"messages":[answer]}



def save_interview(state: InterviewState):
    """Save interviews"""
    messages = state["messages"]
    interview = get_buffer_string(messages)
    return {"interview": interview}


def write_section(state: InterviewState):
    """Node to answer question"""

    interview = state["interview"]
    context = state["context"]
    analyst = state["analyst"]

    if isinstance(analyst, dict):
        analyst = Analyst.model_validate(analyst)

    system_prompt = answer_instructions

    sections = llm.invoke([
        SystemMessage(system_prompt),
        HumanMessage(f"Use this source to write your intstruction: {context}")
    ])

    return {"sections": [sections.content]}


def write_report(state:ResearchGraphState):

    # Full set of sections
    sections = state["sections"]
    topic = state["topic"]

    # Concat all sections together
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])
    
    # Summarize the sections into a final report
    system_message = report_writer_instructions.format(topic=topic, context=formatted_str_sections)    
    report = llm.invoke([SystemMessage(content=system_message)]+[HumanMessage(content=f"Write a report based upon these memos.")]) 
    return {"content": report.content}



def write_introduction(state: ResearchGraphState):
    # Full set of sections
    sections = state["sections"]
    topic = state["topic"]

    # Concat all sections together
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])
    
    # Summarize the sections into a final report
    
    instructions = intro_conclusion_instructions.format(topic=topic, formatted_str_sections=formatted_str_sections)    
    intro = llm.invoke([instructions]+[HumanMessage(content=f"Write the report introduction")]) 
    return {"introduction": intro.content}

def write_conclusion(state: ResearchGraphState):

    # Full set of sections
    sections = state["sections"]
    topic = state["topic"]

    # Concat all sections together
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])
    
    # Summarize the sections into a final report
    
    instructions = intro_conclusion_instructions.format(topic=topic, formatted_str_sections=formatted_str_sections)    
    conclusion = llm.invoke([instructions]+[HumanMessage(content=f"Write the report conclusion")]) 
    return {"conclusion": conclusion.content}

def finalize_report(state: ResearchGraphState):
    """ The is the "reduce" step where we gather all the sections, combine them, and reflect on them to write the intro/conclusion """
    # Save full final report
    content = state["content"]
    if content.startswith("## Insights"):
        content = content.strip("## Insights")
    if "## Sources" in content:
        try:
            content, sources = content.split("\n## Sources\n")
        except:
            sources = None
    else:
        sources = None

    final_report = state["introduction"] + "\n\n---\n\n" + content + "\n\n---\n\n" + state["conclusion"]
    if sources is not None:
        final_report += "\n\n## Sources\n" + sources
    return {"final_report": final_report}