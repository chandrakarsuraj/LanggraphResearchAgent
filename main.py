
from src.create_analyst import graph
from langchain_core.messages import HumanMessage
from rich import print

res = graph.invoke({
    "messages": {
        "topic": "India after 2014",
        "max_analysts": 5,
        "human_analyst_feedback": "no"
    }
})

print(res)