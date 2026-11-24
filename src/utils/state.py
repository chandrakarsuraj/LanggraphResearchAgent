from typing_extensions import TypedDict, Annotated
from typing import List, Optional, NotRequired
from src.utils.objects import Analyst
from langgraph.graph import MessagesState
import operator
# State
class GenerateAnalystSate(TypedDict):
    topic: str 
    max_analysts: int
    human_analyst_feedback: Optional[str]
    analysts : Optional[List[Analyst]]

class InterviewState(MessagesState):
    max_num_turns: int
    context : Annotated[list, operator.add]
    analyst : Analyst
    interview: str 
    sections: list


