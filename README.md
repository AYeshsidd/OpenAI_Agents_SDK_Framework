# Agentic AI & Multi-Agent Framework Exploration 🤖🚀

An advanced, professional-grade repository demonstrating various multi-agent orchestration patterns, safety mechanisms, dynamic system prompting, and interface designs built using the experimental `openai-agents` Python SDK. 

This repository explores the construction of robust, production-ready AI agents using Google's **Gemini 2.0 Flash** model (via OpenAI compatibility), DeepSeek models (via OpenRouter), and local SQLite persistence.

---

## 🗺️ Workspace Map & Project Overview

This workspace is partitioned into three incremental projects, each demonstrating a distinct milestone in the agentic design pattern lifecycle:

```
D:\OpenAI\
├── agents_00/      # Milestone 1: Multi-Agent Hub-and-Spoke Routing & Web Chat UI
├── agents_01/      # Milestone 2: Asynchronous Event Streaming & Dual-Tier Custom Tools
└── agents_02/      # Milestone 3: Safe Multi-Agent Guardrails & Persistent Session Databases
```

---

## 🏗️ Detailed Project Overviews

### 🤖 [agents_00: Multi-Agent Expert Orchestrator & Chat UI](./agents_00)
A foundational hub-and-spoke routing application orchestrating a central router and three domain-specific experts. It supports both command-line testing and interactive web-chat interfaces.
*   **Key Concepts:**
    *   **Hub-and-Spoke Topology:** A central `GeneralAgent` uses the SDK's semantic `handoffs` mechanism to intelligently route queries to localized specialists.
    *   **Specialized Domain Agents:** Includes a *Cooking Expert* (constrained to Pakistani cuisine), a *Maths Expert* (equipped with mathematical computational tools), and an *English Expert* (language teaching assistant).
    *   **Dual Interfaces:** Offers a raw command-line interface (CLI) loop and a Web UI built using **Chainlit** (`chatbot.py`).
    *   **Tooling:** Declarative `@function_tool` bindings for agent computational enhancement.

### ⚙️ [agents_01: Asynchronous Event Streaming & Dynamic Prompting](./agents_01)
A highly modular, professional-grade asynchronous multi-agent framework exploring advanced tooling, dynamic prompt generation, and granular execution event streams.
*   **Key Concepts:**
    *   **Dynamic System Prompts:** Generates customized agent instructions on-the-fly at runtime by passing structured context metadata via a `RunContextWrapper` using Pydantic schema validation.
    *   **Dual-Tier Tool Strategy:**
        *   *High-Level Tools:* Declarative, standard `@function_tool` annotations.
        *   *Low-Level Programmatic Tools:* Custom-instantiated `FunctionTool` constructors providing granular control over JSON validation, input schemas (`tool_schema`), and manual parsing (e.g., negative tense string mutations).
    *   **Asynchronous Event Streaming:** Demonstrates how to run asynchronous loops to intercept intermediate SDK stream events, such as agent transferences (`agent_updated_stream_event`), token-by-token raw response text deltas (`raw_response_event`), and structured stream outputs.
    *   **Multi-LLM-Provider Agnosticism:** Showcases how to easily target different LLM endpoints, utilizing Gemini's compatibility layer or external aggregators like OpenRouter to run reasoning models (DeepSeek-R1).

### 🛡️ [agents_02: Safe Multi-Agent Guardrails & SQLite Persistence](./agents_02)
An enterprise-grade, safe agent setup establishing input/output validation layers around a domain agent (`Cricket Analyst`) and automatically archiving chat history.
*   **Key Concepts:**
    *   **Multi-Agent Guardrail Pattern:** Decouples safety and filtering from the domain specialist. Uses a specialized `Main_guardrail_agent` acting as an active validation filter via custom SDK hooks.
    *   **Input Guardrails (`@input_guardrail`):** Uses structured LLM evaluation to verify user intent and trigger safety tripwires (e.g., blocking off-topic, non-cricket questions) before the core agent processes the prompt.
    *   **Output Guardrails (`@output_guardrail`):** Post-inspects generated responses to detect and censor unauthorized information (e.g., blocking salary disclosures) before final rendering.
    *   **Pydantic Structured Evaluation:** Restricts the guardrail agent to structured JSON schema formatting (`Data_schema`) for reliable downstream logical tripwire evaluations.
    *   **SQLite Session History:** Integrates `SQLiteSession` persistence to automatically store and restore chat histories across terminal executions, avoiding manual buffer management.

---

## 🛠️ Core Technology Stack

*   **Runtime:** Python 3.13+
*   **Orchestration SDK:** `openai-agents` (experimental multi-agent event loop)
*   **Data Validation:** Pydantic (v2)
*   **LLM Providers:** Google Gemini 2.0 (via compatibility layer), OpenRouter (DeepSeek)
*   **Web Frontend:** Chainlit
*   **Database:** SQLite

---

*For in-depth explanations on code patterns, internal schemas, and execution event streams, please consult the respective **README.md** file inside each workspace directory.*
