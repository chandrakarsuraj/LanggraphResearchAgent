
from src.utils.nodes import create_analyst
from rich import print

res = create_analyst({
    "topic": "India after 2014",
    "max_analysts": 5,
    "human_analyst_feedback": "no"
})
print(res)