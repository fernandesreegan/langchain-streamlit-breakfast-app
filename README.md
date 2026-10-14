🍳 LangChain Breakfast Generator

A full-stack interactive LLM application demonstrating core LangChain principles, output object inspection, prompt engineering, and UI performance optimizations using Streamlit.

📌 Project Overview

When invoking a model in LangChain, the invoke() method hands back a complete AIMessage object rather than a raw string. Understanding how to inspect, extract, and constrain these outputs is essential for building production-ready AI applications.

This application provides a two-stage interactive experience:

Stage 1 (Raw Object Inspection): Directly invokes the model and renders the full AIMessage object (including metadata, token counts, and system IDs) without formatting magic.

Stage 2 (Refined Prompt & Macro Controls): Uses a structured ChatPromptTemplate with configurable nutritional constraints (protein, fiber, sugar limits) and extracts clean .content output.

✨ Key Features

Stage 1 — Raw invoke() Inspection:

Visualizes the raw AIMessage return type.

Displays pretty-printed Python object syntax and structured JSON output.

Injects custom CSS auto-wrapping rules to prevent horizontal scrollbar clutter in Streamlit code blocks.

Stage 2 — Refined Prompting & Macro Controls:

Dynamic Nutritional Constraints: Allows users to configure minimum protein, fiber, and maximum sugar thresholds via Streamlit inputs.

Context Switching: Generates tailored options based on context (e.g., Quick weekday morning, Post-workout, Weekend brunch).

Deterministic Sampling: Enforces temperature=0 to reduce generative variance across executions.

Streamlit UI & Performance Optimizations:

Resource Caching (@st.cache_resource): Initializes and caches the ChatOpenAI client in memory once, preventing redundant HTTP connection setups across component updates.

Fragmented Execution (@st.fragment): Wraps individual tabs as isolated components, eliminating full page re-renders when updating input parameters or triggering buttons.

📁 Project Structure

langchain-breakfast-generator/
│
├── app.py              # Main Streamlit application (UI + LangChain logic)
├── .env.example        # Example environment variable file
├── .gitignore          # Ignored files (secrets, virtual environments)
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation


⚡ Quick Start & Installation

1. Prerequisites

Ensure you have Python 3.9+ installed and an active OpenAI API Key.

2. Clone the Repository

git clone https://github.com/YOUR_USERNAME/langchain-breakfast-generator.git
cd langchain-breakfast-generator


3. Set Up Virtual Environment (Recommended)

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate


4. Install Dependencies

pip install -r requirements.txt


5. Environment Setup

Create a .env file in the root directory and insert your OpenAI API key:

OPENAI_API_KEY=your_actual_openai_api_key_here


6. Run the Application

streamlit run app.py


The app will open automatically in your browser at http://localhost:8501.

📝 Assignment Q&A Summary

Question

Analysis / Answer

1. What do you see when printing invoke() directly?

Calling llm.invoke() returns an AIMessage wrapper object rather than a raw string. It contains the generated text inside .content, along with response_metadata (token counts, finish reason, model settings) and an execution id.

2. How to ensure the same 5 ideas every single run?

Set temperature=0 (and optionally specify a fixed seed), tighten system prompt constraints, and use explicit structure definitions to minimize generative sampling variance.

3. What makes a breakfast "healthy" here?

In Stage 1, "healthy" is left to the model's unconstrained training defaults. In Stage 2, "healthy" is strictly defined via explicit system prompt criteria ($\ge 15\text{g}$ protein, $\ge 5\text{g}$ fiber, $< 5\text{g}$ sugar, plus complex carbs/fats).

🛠️ Tech Stack

Language: Python

LLM Orchestration: LangChain (langchain-openai, langchain-core)

Frontend: Streamlit

Model: OpenAI gpt-4o-mini
