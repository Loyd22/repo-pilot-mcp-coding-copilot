# RepoPilot MCP Coding Copilot

RepoPilot is an AI-powered coding assistant that helps developers understand and work with a codebase.

It can explain a repository, read files, search code, summarize Git changes, suggest what to build next, and review the project using an MCP-style tool-calling workflow.

This project is built to demonstrate how an AI assistant can move beyond simple chatbot answers and become a practical developer workflow assistant.

---

## What This Project Does

RepoPilot helps developers answer questions like:

* “Explain this repo.”
* “Show me the repo structure.”
* “Read this file.”
* “Find where this function is used.”
* “What changed in my Git diff?”
* “Is this project production-ready?”
* “What should I build next?”
* “Generate an implementation prompt for Cursor or Codex.”
* “Explain this error.”

Instead of only giving a generic AI answer, RepoPilot first checks the repository using internal tools, then sends the result to the AI model so the final answer is based on actual project context.

---

## Simple Explanation

Think of RepoPilot like a junior developer assistant.

You ask it a question about your codebase.

RepoPilot will:

1. Understand what you are asking.
2. Choose the right tool.
3. Inspect the repository.
4. Send the useful context to the AI model.
5. Return a clear answer.

Example:

```text
User: Explain this repo.

RepoPilot:
1. Loads previous chat memory.
2. Detects that the user wants the repo structure.
3. Reads the project tree.
4. Sends the repo information to OpenAI.
5. Explains the project in simple language.
```

---

## Tech Stack

### Backend

* Python
* FastAPI
* OpenAI Python SDK
* OpenAI Responses API
* LangGraph
* SQLAlchemy
* SQLite
* GitPython

### Frontend

* React
* TypeScript
* Vite

### AI / Agent Workflow

* LangGraph for workflow control
* MCP-style tool calling for repository actions
* OpenAI SDK for AI-generated responses

---

## Important Concepts Used

### OpenAI SDK

This project uses the OpenAI Python SDK to connect the backend to OpenAI models.

Example concept:

```python
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)
```

Simple meaning:

The SDK is the tool that allows the Python backend to communicate with OpenAI more easily.

---

### LangGraph

LangGraph is used to organize the AI workflow into clear steps.

The workflow follows this path:

```text
Start
↓
Load Memory
↓
Classify User Request
↓
Run the Correct Tool
↓
Generate Final Answer
↓
End
```

This makes the assistant more controlled than a normal chatbot.

---

### MCP-Style Tool Calling

This project uses an MCP-style approach.

That means the AI assistant does not directly guess everything. Instead, it uses tools such as:

* Read repository files
* Search the codebase
* Get Git diff
* Review project structure
* Run verification checks
* Create safe edit proposals

Simple meaning:

The AI has “tools” it can use before answering.

---

## Main Features

### 1. Repository Explanation

RepoPilot can explain the structure and purpose of a codebase.

Useful when:

* You are opening a new project.
* You want to understand unfamiliar code.
* You want a quick technical summary.

---

### 2. File Reading

RepoPilot can read specific files from the repository.

Example request:

```text
read backend/app/main.py
```

---

### 3. Code Search

RepoPilot can search for terms inside the project.

Example request:

```text
find OpenAI
```

---

### 4. Git Diff Summary

RepoPilot can check current Git changes and summarize what changed.

Example request:

```text
what changed
```

---

### 5. Production Readiness Review

RepoPilot can review the project for production-readiness signals such as:

* Configuration
* Schema
* Tests
* Logging
* Project structure

Example request:

```text
is this production ready
```

---

### 6. Build-Next Suggestions

RepoPilot can inspect the project and suggest what feature or improvement should be built next.

Example request:

```text
what should I build next
```

---

### 7. Implementation Prompt Generator

RepoPilot can generate a prompt that can be used in tools like Cursor, Codex, or another AI coding assistant.

Example request:

```text
generate implementation prompt
```

---

### 8. Safe Edit Proposal

RepoPilot includes a review-first edit proposal workflow.

Instead of instantly changing code, it can create a safe edit proposal that should be reviewed before applying.

This is useful because AI-generated code changes should be checked before being applied to a real project.

---

## Project Structure

```text
repo-pilot-mcp-coding-copilot/
│
├── backend/
│   └── app/
│       ├── agent/
│       │   ├── graph.py
│       │   ├── nodes.py
│       │   └── state.py
│       │
│       ├── api/
│       │   └── v1/
│       │       └── routes/
│       │
│       ├── core/
│       │   └── config.py
│       │
│       ├── db/
│       │   ├── base.py
│       │   └── session.py
│       │
│       ├── models/
│       │
│       ├── services/
│       │   ├── llm_service.py
│       │   ├── repo_service.py
│       │   ├── git_service.py
│       │   ├── memory_service.py
│       │   ├── edit_service.py
│       │   └── verification_service.py
│       │
│       └── main.py
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
│
├── .env.example
├── requirements.txt
└── README.md
```

---

## How the Backend Works

The backend is the brain of the project.

It uses FastAPI to expose API routes.

When the user sends a message, the backend passes it into the LangGraph workflow.

The workflow has four main steps:

### 1. Load Memory

RepoPilot loads previous messages from the same session.

This helps the assistant understand the recent conversation.

---

### 2. Classify Request

RepoPilot checks the user message and decides the intent.

Example intents:

```text
repo_tree
read_file
search
git_diff
build_next
generate_prompt
explain_error
production_review
propose_edit
verify_repo
unknown
```

---

### 3. Run Tool

Based on the detected intent, RepoPilot runs the correct internal tool.

Example:

If the user asks:

```text
find database
```

RepoPilot runs the search tool.

If the user asks:

```text
what changed
```

RepoPilot runs the Git diff tool.

---

### 4. Generate Final Answer

After the tool returns useful context, RepoPilot sends that context to OpenAI through the OpenAI Python SDK.

The AI then writes a clear final answer based on the repository information.

---

## How the Frontend Works

The frontend provides the user interface for chatting with RepoPilot.

It is built with:

* React
* TypeScript
* Vite

The frontend sends user messages to the backend API and displays the AI assistant’s response.

---

## Environment Variables

Create a `.env` file based on `.env.example`.

Example:

```env
APP_NAME=RepoPilot Backend
APP_ENV=development
APP_DEBUG=true
APP_HOST=127.0.0.1
APP_PORT=8000

FRONTEND_URL=http://localhost:5173

DATABASE_URL=sqlite:///./repopilot.db

OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-5.4
```

Important:

Do not commit your real OpenAI API key to GitHub.

Your API key should stay private.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Loyd22/repo-pilot-mcp-coding-copilot.git
cd repo-pilot-mcp-coding-copilot
```

---

## Backend Setup

### 1. Go to the Backend Folder

```bash
cd backend
```

### 2. Create a Virtual Environment

For Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

For macOS or Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

From the project root or backend setup location, install the Python dependencies:

```bash
pip install -r ../requirements.txt
```

Or if you are in the root folder:

```bash
pip install -r requirements.txt
```

### 4. Run the Backend Server

```bash
uvicorn app.main:app --reload
```

The backend should run at:

```text
http://127.0.0.1:8000
```

---

## Frontend Setup

### 1. Go to the Frontend Folder

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Run the Frontend

```bash
npm run dev
```

The frontend should run at:

```text
http://localhost:5173
```

---

## Example User Prompts

You can test RepoPilot with prompts like:

```text
Explain this repo.
```

```text
repo structure
```

```text
read backend/app/main.py
```

```text
find OpenAI
```

```text
what changed
```

```text
what should I build next
```

```text
generate implementation prompt
```

```text
explain this error: ModuleNotFoundError
```

```text
is this production ready
```

```text
verify repo
```

---

## Example Workflow

```text
User:
Explain this repo.

RepoPilot:
1. Loads memory.
2. Detects the request as repo_tree.
3. Reads the repository structure.
4. Sends the result to OpenAI.
5. Returns a simple explanation of the project.
```

---

## Why This Project Is Useful

RepoPilot is useful because developers often need to understand a codebase quickly.

Instead of manually opening many files, the assistant can inspect the repository and explain the important parts.

This can help with:

* Onboarding into a new project
* Reviewing code changes
* Understanding unfamiliar files
* Preparing implementation plans
* Checking project readiness
* Creating better prompts for AI coding tools

---

## What I Learned From This Project

This project helped me practice:

* Building a FastAPI backend
* Using the OpenAI Python SDK
* Calling the OpenAI Responses API
* Creating an AI workflow with LangGraph
* Designing MCP-style tool calling
* Reading and searching a codebase programmatically
* Managing chat memory
* Structuring backend services
* Connecting a React frontend to a Python backend

---

## Future Improvements

Possible improvements for this project:

* Add a real MCP server/client implementation
* Improve edit proposal generation
* Add authentication
* Add user project workspaces
* Add file upload support
* Add better frontend UI for tool traces
* Add automated tests
* Add Docker support
* Add deployment configuration
* Add streaming AI responses
* Add better error handling
* Add support for multiple repositories
* Add approval workflow for applying code edits

---

## Resume Description

You can describe this project on your resume like this:

```text
Built RepoPilot, an AI-powered repository assistant using FastAPI, React, LangGraph, and the OpenAI Python SDK. The system analyzes codebases, reads files, searches repository content, summarizes Git changes, and uses MCP-style tool calling to support developer workflows.
```

---

## Interview Explanation

If an interviewer asks about this project, you can say:

```text
RepoPilot is an AI coding copilot that helps developers understand and work with a repository. I built a FastAPI backend and React frontend, then used LangGraph to organize the AI workflow into steps like loading memory, classifying the request, running the correct repository tool, and generating the final answer. I also used the OpenAI Python SDK to call the OpenAI Responses API. The project demonstrates MCP-style tool calling because the assistant can use tools like repo search, file reading, Git diff, verification, and production review before answering.
```

---

## Important Note

This project currently uses MCP-style tool calling, but it is not yet a full official MCP implementation unless an actual MCP server/client is added.

A more accurate description is:

```text
AI repository assistant with LangGraph workflow and MCP-style tool calling.
```

---

## Author

Created by John Loyd Viray.

GitHub: Loyd22
