# Agentic Multi-Agent Framework

A professional-grade, asynchronous multi-agent orchestration framework built with the `openai-agents` SDK and Python 3.13+. This project demonstrates advanced agentic workflows, including dynamic contextual instruction injection, type-safe state management, custom low-level and high-level tool integration, multi-agent handoffs, and real-time execution streaming over diverse LLM backends (Google Gemini API and OpenRouter).

---

## 🏗️ Architectural Overview

The architecture follows a decoupled, event-driven pattern designed for high modularity, scalability, and type safety:

```
                  ┌──────────────────────────────┐
                  │         User Input           │
                  └──────────────┬───────────────┘
                                 ▼
                     ┌───────────────────────┐
                     │     General Agent     │ (Orchestrator & Router)
                     │   (Orchestrates handoffs)
                     └──────┬────┬────┬──────┘
                            │    │    │
         ┌──────────────────┘    │    └───────────────────┐
         ▼                       ▼                        ▼
┌─────────────────┐    ┌──────────────────┐     ┌───────────────────┐
│  Math Agent     │    │  Cooking Agent   │     │   English Agent   │ (Specialists)
├─────────────────┤    ├──────────────────┤     ├───────────────────┤
│ - Dynamic Inst. │    │ - Strict Guards  │     │ - Custom Low-Level│
│ - Math Tools    │    │                  │     │   Tense Tool      │
└─────────────────┘    └──────────────────┘     └───────────────────┘
```

### Key Design Pillars

1. **Multi-Agent Orchestration (Handoff Pattern)**:
   A parent `GeneralAgent` functions as a central router. Using semantic intent parsing, it hands off execution to specialized child agents (`Maths Expert`, `Cooking Expert`, `English Expert`) via SDK-managed handoffs.
2. **Context-Driven Dynamic Prompting**:
   System instructions are not hardcoded. They are dynamically generated at runtime via structured context wrapper (`RunContextWrapper`) and Pydantic schema validation.
3. **Dual-Tier Tool Strategy**:
   - **Declarative High-Level Tools**: Generated automatically using `@function_tool` decorators based on standard Python functions.
   - **Programmatic Low-Level Tools**: Created manually via `FunctionTool` constructor to offer granular control over JSON validations, custom schemas, and direct execution overrides.
4. **Asynchronous & Real-Time Stream Event Loop**:
   Demonstrates how to listen to intermediate agent lifecycle updates, raw streaming text deltas, and token-by-token UI/UX execution nodes.
5. **Multi-Provider LLM Abstraction**:
   Supports unified execution over multiple endpoints, showcasing Google Gemini's OpenAI compatibility layer and OpenRouter (running DeepSeek reasoning models).

---

## 📂 Codebase Structure & File Analysis

```
.
├── pyproject.toml             # Python package dependencies & tool settings
├── main.py                    # Main app loop, Gemini setup, Agents & Streaming logic
├── README.md                  # System architecture & developer guidelines
├── Instruction/
│   └── dynamic_work.py        # Dynamic contextual instruction resolver
├── open_router/
│   └── index.py               # Alternative OpenRouter (DeepSeek) agent workflow
└── Tools/
    └── tools.py               # Shared tool definitions (Math, Tenses, Context Schemas)
```

### 1. Configuration (`pyproject.toml`)
Defines python requirements (`>=3.13`) and key dependency libraries:
* `openai`: Core SDK for models interface.
* `openai-agents`: Orchestration library for executing multi-agent loops.
* `python-dotenv`: Environment variable management.

### 2. Main Coordinator (`main.py`)
Sets up the API clients for **Gemini-2.0-Flash** via OpenAI's compatibility layer. Configures and initializes:
* **`cooking_agent`**: Focused solely on Pakistani cuisine under strict guardrails.
* **`Math_agent`**: Integrated with math function tools and runtime-dynamic system instructions.
* **`English_agent`**: Armed with custom grammatical conversion capabilities.
* **`General_agent`**: Orchestrates global routing with `handoffs` registered to all specialized sub-agents.
* **Execution Engines**: Showcases multiple running behaviors including synchronous runner loops and structured async streaming event checks (commented blocks).

### 3. Dynamic Context (`Instruction/dynamic_work.py`)
Houses runtime-injection system logic. Contains the `dynamic` callback which transforms structured metadata payload into highly personalized, target instructions for active LLMs.

### 4. OpenRouter Agent (`open_router/index.py`)
Demonstrates how to run alternative pipelines on external API aggregators. Connects to `deepseek/deepseek-r1-0528:free` model using `OpenAIChatCompletionsModel` to direct an `English professor` and `Travel agent` flow.

### 5. Tools Registry (`Tools/tools.py`)
The functional engine of the framework. Contains:
* Schemas for validation (`user_data`, `tool_schema`).
* Multi-tier tool definitions (Custom Programmatic Tools + Decorated Utility Tools).

---

## 🛠️ Important Methods & Schemas Reference

### Type-Safe Models & Schemas

#### `user_data` (Pydantic Model)
Stores structural runtime context passed down to agents and tool operations.
```python
class user_data(BaseModel):
    name: str
    Field: str
    age: int
```

#### `tool_schema` (Pydantic Model)
Defines incoming string payloads for low-level manual tools.
```python
class tool_schema(BaseModel):
    sentense: str
```

---

### Agent System Methods

#### `dynamic(ctx, agent)` (Dynamic System Instructions)
Generates personalized system prompt injection on-the-fly.
* **Signature**: `dynamic(ctx: RunContextWrapper[user_data], agent: Agent[user_data]) -> str`
* **File**: `Instruction/dynamic_work.py` (and commented equivalent in `Tools/tools.py`)
* **Logic**: Intercepts `ctx.context` to embed the user's name, field of study, and age dynamically into the maths teacher instructions.

---

### Standard Math Tools (`@function_tool`)
Automatically parsed into OpenAI-compatible tools using parameter annotations.
* **File**: `Tools/tools.py`

#### `plus_numbers(a, b)`
* **Inputs**: `a: int`, `b: int` -> Returns sum `a + b` as string formatted answer.

#### `subtract_numbers(a, b)`
* **Inputs**: `a: int`, `b: int` -> Returns difference `a + -b` (negative addition).

#### `divide_numbers(a, b)`
* **Inputs**: `a: int`, `b: int` -> Returns division result `a / b`.

---

### Specialized Grammatical Tool (Manual `FunctionTool`)
Demonstrates manual schema mapping and internal payload parsing.
* **File**: `Tools/tools.py`

#### `negative_tense` (Coroutine)
* **Signature**: `async def negative_tense(ctx: RunContextWrapper, arg: str) -> str`
* **Logic**: Receives a raw JSON string `arg` from the model, validates it against `tool_schema` using `.model_validate_json(arg)`, parses the sentence words, checks against common English auxiliary verbs list (`am`, `is`, `are`, `was`, `were`, `will`, `shall`, etc.), inserts `"not"` dynamically to convert the sentence into its negative counterpart, and returns the constructed string.

#### `tense` (Manual instantiation)
* **Object**: `FunctionTool`
* **Logic**: Binds `negative_tense` to the agent pipeline manually, passing the parameters schema explicitly using `tool_schema.model_json_schema()`.

---

### Context Retrieval Tool (Commented Out)
#### `get_age(ctx)`
* **Signature**: `def get_age(ctx: RunContextWrapper[user_data]) -> str`
* **File**: `Tools/tools.py`
* **Logic**: Shows how an agent can inspect internal type-safe context wrapper during active tool calling to report details such as user age.

---

### Runner and Event Streaming Strategies
These methods coordinate workflow execution and are defined in `main.py` (in active loop and commented streaming setups).

#### 1. Synchronous Runner Loop
Runs queries synchronously on a designated agent.
```python
agent_Response = Runner.run_sync(
    Math_agent,
    input=prompt,
    context=user_Info,
    run_config=config,
)
print(agent_Response.final_output)
```

#### 2. Asynchronous Multi-Turn Runner (Commented)
Supports running general routing multi-turn pipelines concurrently.
```python
agent_Response = await Runner.run(
    General_agent,
    prompt,
    run_config=config,
    max_turns=7
)
print(agent_Response.final_output)
```

#### 3. Agent Update Stream Event Listener (Commented)
Subscribes to agent transitions/handoff events in streaming.
```python
agent_Response = Runner.run_streamed(General_agent, prompt, run_config=config)
async for checking_events in agent_Response.stream_events():
    if checking_events.type == "agent_updated_stream_event":
        print(f"Agent update: {checking_events.new_agent.name}")
```

#### 4. Raw Response Text Delta Stream Listener (Commented)
Renders individual token deltas as they stream from the LLM endpoint.
```python
agent_Response = Runner.run_streamed(Math_agent, prompt, run_config=config)
async for checking_events in agent_Response.stream_events():
    if checking_events.type == "raw_response_event" and isinstance(checking_events.data, ResponseTextDeltaEvent):
        print(checking_events.data.delta, end="", flush=True)
```

#### 5. High-Level Item Output Stream Listener (Commented)
Resolves structured outputs and items within the streaming run using standard helpers.
```python
agent_Response = Runner.run_streamed(General_agent, prompt, run_config=config)
async for checking_events in agent_Response.stream_events():
    if checking_events.type == "run_item_stream_event":
        if checking_events.item.type == "message_output_item":
            print(f"---Message Output:\n {ItemHelpers.text_message_output(checking_events.item)}")
```

---

## ⚡ Setup & Execution

### Prerequisites
* Python `3.13` or higher.
* [uv](https://github.com/astral-sh/uv) (Recommended Python package management tool) or `pip`.

### 1. Environment Configuration
Create a `.env` file in the root directory and supply your api keys:
```env
GEMINI_API_KEY=your_google_gemini_api_key
GEMINI_BASE_PATH=https://generativelanguage.googleapis.com/v1beta/openai/

# Required if running open_router/index.py
OPENROUTER_API_KEY=your_open_router_api_key
```

### 2. Dependency Installation
Using **uv**:
```bash
uv sync
```
Using **pip**:
```bash
pip install -r pyproject.toml
# Or standard dependency installs:
pip install openai openai-agents python-dotenv pydantic
```

### 3. Execution
To run the main Gemini multi-agent system:
```bash
python main.py
```

To run the alternative OpenRouter DeepSeek routing workflow:
```bash
python open_router/index.py
```
