from typing_extensions import TypedDict
from typing import List, Optional, NotRequired
from src.utils.objects import Analyst

# State
class GenerateAnalystSate(TypedDict):
    topic: str 
    max_analysts: int
    human_analyst_feedback: Optional[str]
    analysts : Optional[List[Analyst]]