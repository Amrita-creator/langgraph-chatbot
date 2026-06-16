# LangGraph Chatbot

A conversational chatbot application powered by **LangGraph** (StateGraph), **LangChain**, and **Llama-3.1-8B-Instruct** (via Hugging Face Endpoint), featuring a clean, responsive **Streamlit** user interface.

## Features

- **Interactive Chat Interface:** Standardized Streamlit chat interface with message bubbles and user/assistant formatting.
- **State Preservation:** Powered by LangGraph's `SqliteSaver` checkpointer, meaning conversations are automatically saved in a local SQLite database (`chatbot.db`) and persisted across app runs.
- **Multi-thread/Multi-conversation Support:** Switch between previous chat threads or start a "New Chat" instantly using the sidebar.
- **Streaming Responses:** Assistant replies stream in real-time.

---

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/Amrita-creator/langgraph-chatbot.git
cd langgraph-chatbot
```

### 2. Create and activate a Virtual Environment
```bash
# Create
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the root directory and add your Hugging Face API Token:
```env
HUGGINGFACEHUB_API_TOKEN=your_huggingface_api_token_here
```

---

## Running the Application

Start the Streamlit application using:
```bash
streamlit run frontend.py
```
Open the local URL (usually `http://localhost:8501`) in your browser to start chatting!

---

## Repository Structure

- `frontend.py`: Main Streamlit UI handling user interaction, layout, and streaming history.
- `langgraph_backend.py`: StateGraph model definition, Hugging Face client initialization, and SQLite checkpointer configuration.
- `requirements.txt`: Package dependencies.
- `.gitignore`: Specifying ignored folders (like `venv/`, `.env`, and `chatbot.db`).
- `TEST.py`: A script to test the connection to the Hugging Face model endpoint.
