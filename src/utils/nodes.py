

from dotenv import load_dotenv
from src.utils.state import GenerateAnalystSate
from typing import Dict, Any
from src.utils.models import llm
from src.utils.objects import Perspective
from src.utils.prompts import analyst_instructions
from langchain_core.messages import HumanMessage, AIMessage,SystemMessage
from langgraph.types import interrupt

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