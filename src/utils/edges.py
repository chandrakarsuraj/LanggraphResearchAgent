from dotenv import load_dotenv
from src.utils.state import GenerateAnalystSate
from typing import Literal
from langgraph.graph import END
load_dotenv()


# conditional edges
def should_continue(state:GenerateAnalystSate):
    """Return the next node to execute"""

    human_analyst_feedback = state.get("human_analyst_feedback", None)

    if human_analyst_feedback:
        return "create_analyst"

    return END

