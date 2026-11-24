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
    max_num_turns: NotRequired[int]
    context: Annotated[list[str], operator.add]
    analyst: Analyst
    interview: NotRequired[str]
    sections: NotRequired[list[str]]


class ResearchState(TypedDict):

    topic: str 
    max_analysts: int
    human_analyst_feedback: Optional[str]
    analysts : Optional[List[Analyst]]


class ResearchGraphState(TypedDict):
    topic: str # Research topic
    max_analysts: int # Number of analysts
    human_analyst_feedback: NotRequired[Optional[str]] # Human feedback
    analysts: List[Analyst] # Analyst asking questions
    sections: Annotated[list, operator.add] # Send() API key
    introduction: str # Introduction for the final report
    content: str # Content for the final report
    conclusion: str # Conclusion for the final report
    final_report: str # Final report