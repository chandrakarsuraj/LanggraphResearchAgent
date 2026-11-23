

from dotenv import load_dotenv
from src.utils.state import GenerateAnalystSate
from typing import Dict, Any
from src.utils.models import llm
from src.utils.objects import Perspective
from src.utils.prompts import analyst_instructions
from langchain_core.messages import HumanMessage, AIMessage,SystemMessage

load_dotenv()


# nodes

def create_analyst(state:GenerateAnalystSate)->Dict[str, Any]:
    """Create analyst"""
    topic = state["topic"]
    max_analyst = state["max_analysts"]
    human_analyst_feedback = state["human_analyst_feedback"]

    # Enforce Structere Output
    structured_llm = llm.with_structured_output(Perspective)


    # System message
    
    messages = [
        SystemMessage( analyst_instructions),
        HumanMessage(f""" 
            Topic: {topic},
            Human Analyst Feedback: {human_analyst_feedback},
            Max Analyst : {max_analyst}
        """)
    ]

    res = structured_llm.invoke(messages)
    return {"analysts": res.analysts}
