# Agentic Guard: Safe Cricket Analyst Agent

An asynchronous, console-based conversational AI application that serves as a professional **Cricket Analyst**. This project demonstrates the usage of the experimental `openai-agents` framework combined with structured Pydantic schemas, local SQLite session history, and rigorous input/output guardrails backed by Google's **Gemini 2.0 Flash** model (via its OpenAI-compatible endpoint).

---

## 🏛️ System Architecture

The application implements a multi-agent guardrail pattern to isolate and protect the main domain agent (`Cricket Analyst`) from unsafe, irrelevant, or off-topic interactions.

```
       [ User Input ]
             │
             ▼
┌───────────────────────────┐
│  Input Guardrail Hook     │
│  (guardrail_input)        │
└────────────┬──────────────┘
             │
             ├─► [Runs Guardrail Agent] ──► Checks user intent (is_cricket_query?)
             │                                   │
             ▼                                   ▼
      [Tripwire Triggered?] ──(Yes)──► [InputGuardrailTripwireTriggered Exception]
             │ (No)
             ▼
┌───────────────────────────┐
│   Cricket Analyst Agent   │ ◄── [SQLite Session Memory] (Restores Chat Context)
│      (cricket_agent)      │
└────────────┬──────────────┘
             │ (Generates Response)
             ▼
┌───────────────────────────┐
│  Output Guardrail Hook    │
│  (guardrail_output)       │
└────────────┬──────────────┘
             │
             ├─► [Runs Guardrail Agent] ──► Checks output safety (salary_related_query?)
             │                                   │
             ▼                                   ▼
      [Tripwire Triggered?] ──(Yes)──► [OutputGuardrailTripwireTriggered Exception]
             │ (No)
             ▼
    [ Display Response ]
```

---

## 💡 Core Agentic Concepts

### 1. Multi-Agent Evaluation & Guardrails
Instead of embedding safety/classification logic directly inside the domain analyst's instructions, safety is delegated to a specialized **`Main_guardrail_agent`**. 
- **Input Guardrails (`@input_guardrail`)**: Validates prompts before they are processed by the core LLM agent. If the evaluation determines the query is off-topic, it trips the input guardrail.
- **Output Guardrails (`@output_guardrail`)**: Post-inspects the generated response before displaying it to the user. This ensures sensitive or restricted information (such as players' salaries) is blocked before reaching the output terminal.

### 2. Structured LLM Responses (Pydantic Integration)
The `Main_guardrail_agent` is configured with `output_type=Data_schema`. This guarantees that its evaluation returns a structured Pydantic object containing precise classifications, allowing programmatically clean tripwire checks:
- `is_cricket_query` (boolean classification)
- `salary_related_query` (boolean classification)
- `Expert_opinion` (string analysis context)

### 3. SQLite Session Management
Using `SQLiteSession`, conversation histories are persisted locally in an SQLite database. This manages context windows automatically, allowing the domain agent to carry on multi-turn conversations seamlessly across executions.

---

## 📂 File Directory

```
D:\OpenAI\agentic_02\
├── main.py                    # Application entrypoint, agent setups, guardrail hooks, CLI loop
├── guardrail_schema/
│   └── data.py                # Schema definitions (Data_schema) using Pydantic
├── pyproject.toml             # Project metadata and packages (openai-agents)
└── uv.lock                    # Dependency lockfile
```

---

## 🛠️ Key Classes and Methods

### Schema Definition (`guardrail_schema/data.py`)
* `Data_schema(BaseModel)`: Define constraints for the Guardrail Agent.
  * `is_cricket_query: bool` - Identifies if prompt belongs to cricket.
  * `salary_related_query: bool` - Detects if the response mentions salary structures.
  * `Expert_opinion: str` - Explanatory remarks or analysis.

### Main Execution (`main.py`)
* `Main_guardrail_agent`: A structured output agent specialized in classification tasks.
* `guardrail_input(ctx, agent, input)`:
  - Invokes `Main_guardrail_agent` with the user's prompt.
  - Returns `GuardrailFunctionOutput`. Sets `tripwire_triggered = not result.final_output.is_cricket_query` to block off-topic prompt execution.
* `guardrail_output(ctx, agent, output)`:
  - Invokes `Main_guardrail_agent` with the assistant's generated output.
  - Returns `GuardrailFunctionOutput`. Sets `tripwire_triggered = result.final_output.salary_related_query` to censor financial details.
* `cricket_agent`: The primary analyst agent loaded with expert cricketing instructions, bound with both the input and output guardrails.
* `Runner.run(...)`: Orchestrates the asynchronous execution pipeline of agents under a designated session context.

---

## 🔍 Important Commented Code Notes

1. **`tripwire_triggered=True`**:
   Inside both `guardrail_input` and `guardrail_output`, comments specify:
   `# tripwire_triggered=True, if True that means bad input from user`. 
   This shows how setting this parameter to `True` terminates execution and triggers the corresponding framework exceptions.
2. **`salary_related_query` guard**:
   `# ye guard kry ga salary related query ko` (Urdu translation: *This will guard salary-related queries*). Indicates that financial disclosures are strictly forbidden.
3. **`tool_use_behavior="stop_on_first_tool"`**:
   Commented out inside the `cricket_agent` configuration. If enabled, this parameter halts the agent's workflow immediately when a tool is called, which is useful for debugging tool invocations, collecting human-in-the-loop approvals, or orchestrating manual execution steps.

---

## 🚀 Setup & Usage

1. **Environment Config**:
   Create a `.env` file containing:
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   GEMINI_BASE_PATH=https://generativelanguage.googleapis.com/v1beta/openai/
   ```

2. **Install Dependencies**:
   ```bash
   uv sync
   ```

3. **Run CLI**:
   ```bash
   uv run main.py
   ```
