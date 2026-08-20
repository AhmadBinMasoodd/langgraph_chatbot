# LangGraph Chatbot

A simple conversational chatbot built with [LangGraph](https://langchain-ai.github.io/langgraph/), LangChain, Groq, and Streamlit.

The project contains:

- `backend.py`: Defines and compiles a LangGraph chatbot with an in-memory checkpointer.
- `frontend.py`: Provides the Streamlit chat interface and preserves the visible message history during the session.
- `requirements.txt`: Lists the Python dependencies.

## Requirements

- Python 3.9 or later
- A Groq API key

## Setup

1. Create and activate a virtual environment:

	```bash
	python -m venv .venv
	```

	Windows PowerShell:

	```powershell
	.venv\Scripts\Activate.ps1
	```

2. Install the dependencies:

	```bash
	pip install -r requirements.txt
	```

3. Create a `.env` file in the project root and add your Groq API key:

	```env
	GROQ_API_KEY=your_groq_api_key
	```

## Run the chatbot

Start the Streamlit application from the project directory:

```bash
streamlit run frontend.py
```

Streamlit will display a local URL in the terminal. Open that URL in a browser and enter a message in the chat input.

## How it works

The backend creates a `StateGraph` with one chat node. The node sends the conversation messages to the Groq model and returns the assistant response. The graph uses an `InMemorySaver` checkpointer with a fixed thread ID, so conversation context is retained while the application process is running. Restarting the app clears the in-memory conversation state.

## Configuration

The model is configured in `backend.py`:

```python
model="openai/gpt-oss-20b"
temperature=0
```

To use another Groq-supported model, update the `model` value in that file.
