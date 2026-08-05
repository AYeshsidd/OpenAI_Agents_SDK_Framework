# Multi-Agent Expert Orchestrator 🤖💬

A Python-based multi-agent system utilizing the `openai-agents` framework to intelligently route, process, and resolve specialized user queries. The system orchestrates interaction between multiple domain-specific agents—Cooking, Mathematics, and English—coordinated by a central routing agent, and includes support for both command-line and web-based (Chainlit) interfaces.

---

## 🏗️ Architecture & Project Structure

The codebase is organized as follows:

*   **`main.py`**: The core application logic containing the agent configurations, instructions, routing logic (handoffs), and sync/async runner logic.
*   **`tools.py`**: Defined utility functions decorated with `@function_tool` (e.g., math utilities for addition and subtraction) invoked dynamically by the agents.
*   **`chatbot.py`**: A lightweight Chainlit web frontend template providing a webchat interface for user interactions.
*   **`config_file.py`**: Alternative configurations for utilizing alternative API endpoints and model parameters (e.g., Gemini-compatible endpoints).
*   **`pyproject.toml`**: Project package specification and dependency configurations (requires `chainlit`, `dotenv`, and `openai-agents`).
*   **`chainlit.md`**: Configuration of the greeting/welcome screen inside the Chainlit web interface.

---

## 👥 Agent Hierarchy & Routing

The system employs a hub-and-spoke multi-agent routing topology:

```
                  ┌─────────────────┐
                  │  General Agent  │ (Orchestration Router)
                  └────────┬────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
┌────────────────┐ ┌───────────────┐ ┌────────────────┐
│ Cooking Expert │ │ Maths Expert  │ │ English Expert │
└────────────────┘ └───────┬───────┘ └────────────────┘
                           │ (Equipped Tools)
                           ▼
                 ┌───────────────────┐
                 │ my_tool / my_tool2│
                 └───────────────────┘
```

1.  **General Agent (`GeneralAgent`)**: The gateway router. Evaluates user input and utilizes the `handoffs` mechanism to delegate queries to the correct domain expert.
2.  **Cooking Expert (`Cooking Expert`)**: Pakistani culinary specialist. Constrained to Pakistani dishes and food-related queries (limited responses up to 5 lines).
3.  **Maths Expert (`Maths Expert`)**: Core math operations agent. Equipped with function tools for accurate computations (`my_tool` for addition and `my_tool2` for subtraction).
4.  **English Expert (`English Expert`)**: Language pedagogy assistant designed to teach English concepts.

---

## 🚀 Getting Started

### 📋 Prerequisites

*   Python `3.13` or higher.
*   [uv](https://github.com/astral-sh/uv) (recommended) or `pip` for package management.

### ⚙️ Setup and Installation

1.  **Clone or navigate to the project directory:**
    ```bash
    cd D:\python_work\agent_exam
    ```

2.  **Create a virtual environment and install dependencies:**
    Using `uv`:
    ```bash
    uv sync
    ```
    Or using standard `pip`:
    ```bash
    pip install -r pyproject.toml
    ```

3.  **Configure Environment Variables:**
    Create a `.env` file in the root directory (or update the existing one) with your API credentials:
    ```env
    OPENAI_API_KEY="your-openai-api-key-here"
    ```

---

## 💻 Running the Application

### Option A: Command Line Interface (CLI)

Executes the agent orchestrator directly in the console:

```bash
python main.py
```

### Option B: Chainlit Web Interface

Serves a browser-based conversational interface (auto-reloads on edits with `-w` flag):

```bash
chainlit run chatbot.py -w
```

---

## 🛠️ Codebase Analysis & Recommended Revisions

During our code inspection, the following technical and architectural improvements were identified for the next development iteration:

1.  **Unified Chainlit & Agent Integration (`chatbot.py`):**
    Currently, `chatbot.py` operates as a simple echo server and does not import or invoke the `General_agent` from `main.py`. It should be revised to run the agent asynchronously on message events to enable chat-based orchestration.
2.  **Strict Typing & Tool Typo (`tools.py`):**
    In `tools.py`, the subtraction helper returns `a +- b`, which mathematically evaluates to `a - b` but is non-standard. This should be cleaned to `a - b`.
3.  **Instruction Consistency (`main.py`):**
    *   `English_agent` instructions contain copy-paste remnants referencing cooking/food, which should be removed.
    *   `English_agent` instructions request calling `my_tool` for addition, but the agent does not have `my_tool` registered in its `tools` list.
    *   Ensure consistent quote escaping in agent instructions to avoid parsing warnings.
