# LangGraph Research Agent

A LangGraph application that builds a research report from a topic. It generates a panel of analyst personas, pauses for human review, runs parallel research interviews with web search, and assembles the results into a Markdown report.

## How it works

The main report workflow is currently registered as `create_analyst`:

1. **Create analysts** — use the topic and requested analyst count to generate distinct research perspectives.
2. **Human review** — pause for approval or feedback. Feedback other than an approval response is sent back to analyst generation.
3. **Parallel interviews** — launch an interview for each approved analyst. Each interview generates questions, searches the web, answers using retrieved context, and writes a section.
4. **Build the report** — combine the interview sections into a report, generate an introduction and conclusion, and include the collected sources.

The interviewer graph uses LangGraph's `Send` API to fan out work across analysts. The interview graph asks follow-up questions until it reaches its turn limit (2 by default) or the interview signals completion.

## Project layout

```text
.
├── langgraph.json             # LangGraph app and graph registry
├── main.py                    # Hard-coded example invocation
└── src/
    ├── create_analyst.py      # Full analyst-to-report workflow
    ├── qa_agent.py            # Interview subgraph
    ├── research_agent.py      # Interview graph variant
    └── utils/
        ├── edges.py           # Conditional routing and interview fan-out
        ├── models.py          # Chat model configuration
        ├── nodes.py           # Analyst, search, interview, and report nodes
        ├── objects.py         # Pydantic schemas for analysts and search queries
        ├── prompts.py         # Model instructions
        └── state.py           # LangGraph state schemas
```

### Registered graphs

The graph IDs in `langgraph.json` are:

| Graph ID | Source | Purpose |
| --- | --- | --- |
| `create_analyst` | `src/create_analyst.py` | Full workflow, from analyst creation through report finalization |
| `que_n_ans` | `src/qa_agent.py` | Interview subgraph |
| `research_agent` | `src/research_agent.py` | Interview graph variant |

Despite its name, the registered `research_agent` graph is currently the interview graph; use `create_analyst` for the end-to-end report workflow.

## Requirements

- Python 3.12 or later
- [uv](https://docs.astral.sh/uv/)
- OpenAI and Tavily API credentials

## Setup

Install the project dependencies from the lockfile:

```bash
uv sync
```

Create or update the root `.env` file with the credentials used by the integrations:

```dotenv
OPENAI_API_KEY=your-openai-api-key
TAVILY_API_KEY=your-tavily-api-key
```

The chat model is configured in `src/utils/models.py` (`gpt-6-luna` at present). Change that setting if you want to use a different model available to your OpenAI account.

## Run locally

Start the LangGraph development server from the repository root:

```bash
uv run langgraph dev
```

Open the local development UI and select the `create_analyst` graph. Start a run with input such as:

```json
{
  "topic": "India after 2014",
  "max_analysts": 5
}
```

The workflow pauses at human review. Approve the generated analyst panel to continue, or provide feedback to regenerate it. The graph server provides the persistence and resume flow for this interrupt.

## Notes

- `main.py` is a small hard-coded invocation example, not a configurable command-line interface. The LangGraph development server is the recommended way to run the human-in-the-loop workflow.
- Search results are supplied as context to the interview-answer node; the answer prompt instructs the model to ground its response in that context and cite sources.
- Treat generated analyst profiles and report content as AI-generated research drafts. Verify important claims and citations against the linked sources.
