# AI Agent Development

A hands-on, day-by-day Python course for building **conversational AI assistants and local AI agents** with Python and Ollama. Each folder (`day01`–`day07`) adds one layer: Q&A, memory, system prompts, tools, file reading, RAG retrieval, and **LLM-based tool planning**.

The stack uses the [OpenAI Python SDK](https://github.com/openai/openai-python) against a compatible API—typically [Ollama](https://ollama.com) running locally.

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) (or another OpenAI-compatible endpoint)
- Chat model pulled in Ollama (for example `llama3.2`, `qwen2.5`, or your course model)
- For Day 06: an embedding model (for example `nomic-embed-text`)

```bash
ollama pull <your-chat-model>
ollama pull nomic-embed-text   # Day 06 embeddings
```

## Setup

1. Clone the repository and create a virtual environment:

```bash
cd ai-agent-development
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install openai python-dotenv numpy
```

3. Create a `.env` file in the project root (see `.gitignore`; never commit secrets):

```env
BASE_URL=http://localhost:11434/v1
API_KEY=ollama

# Used by day01–day05 and day02 thinking demo
MODEL=your-chat-model

# Day 06–07 chat assistant and Day 07 planner
CHAT_MODEL=your-chat-model

# Day 06 embeddings / RAG
EMBEDDING_MODEL=nomic-embed-text
```

4. Run scripts from the **repository root** so paths like `day06/knowledge/` resolve correctly.

### Quick start (latest day)

```bash
python day07/assistant.py
```

Other days: `python day0N/ai_assistant.py` where present, `python day07/assistant.py` for the planner agent, and `python day01/hello_ai.py` for the first one-shot demo.

## Learning path (by commit)

| Day | Focus | Main entry points |
|-----|--------|-------------------|
| **Day 01** | First call to the model; interactive Q&A loop | `day01/hello_ai.py`, `day01/ai_assistant.py` |
| **Day 02** | Conversation memory (`messages_history`) | `day02/ai_assistant.py` |
| **Day 02+** | Reasoning models: parse `redacted_thinking` tags from responses | `day02/ai_assistant_with_thinking.py` |
| **Day 03** | System prompts and selectable personalities | `day03/ai_assistant.py`, `day03/util.py` |
| **Day 04** | Python “tools” (time, dice, password) wired into the loop | `day04/tools.py`, `day04/ai_assistant.py`, `day04/tools_manager.py` |
| **Day 05** | Read `.txt` files and inject content into the user message | `day05/tools.py`, `day05/ai_assistant.py`, sample data in `day05/data/` |
| **Day 06** | RAG workflow: knowledge base, keyword vs embedding retrieval | `day06/retriever.py`, `day06/similarity.py`, `day06/test_embedding.py`, `day06/test_retriever.py` |
| **Day 07** | AI planner + tool agent (plan → execute → natural answer) | `day07/planner.py`, `day07/assistant.py`, `day07/tools.py`, `day07/test_planner.py` |

Type `quit` at the prompt to exit interactive assistants (including `day07/assistant.py`).

### Day 01 — Basic assistant

- `hello_ai.py`: one-shot question (“What is Artificial Intelligence?”).
- `ai_assistant.py`: REPL that sends each user turn to the model with Ollama-friendly `extra_body` options (`num_predict`, `temperature`).

### Day 02 — Memory

- `ai_assistant.py`: appends user and assistant messages to `messages_history` so the model sees prior turns.
- `ai_assistant_with_thinking.py`: optional display of model “thinking” tags before the final answer; keeps full assistant content in history for context.

### Day 03 — Personalities

- Choose a system persona at startup (Patient Tutor or Daily Lifestyle Coach) via `get_user_choice()` in `util.py`.
- System message is the first entry in `messages_history`.

### Day 04 — Tools

- `tools.py`: `get_current_time()`, `roll_dice()`, `generate_password()`.
- `ai_assistant.py`: simple keyword routing (e.g. time-related input) before calling the model.
- `tools_manager.py`: small script to exercise the tools without the chat loop.

### Day 05 — File reading

- `read_text_file()` loads local text files.
- `alter_user_input()` detects a `.txt` path in the user message, replaces it with file contents, then sends the enriched text to the model.
- Sample files: `day05/data/notes.txt`, `day05/data/code.txt`.

This approach highlights limits (single-file regex, large files, context size)—motivation for Day 06 retrieval.

### Day 06 — RAG building blocks

Knowledge documents live in `day06/knowledge/` (company policy, product manual, customer support, technical FAQ).

| Module | Role |
|--------|------|
| `similarity.py` | Cosine similarity between embedding vectors (NumPy) |
| `test_embedding.py` | Ollama embeddings via `EMBEDDING_MODEL`; `get_embedding_vector(question, content)` |
| `retriever.py` | `load_documents()` from `day06/knowledge/*.txt`; `retrieve()` (keyword); `retrieve_based_on_embedding()` (best match by similarity) |
| `test_retriever.py` | Demo embedding-based retrieval (e.g. query “amazon”) |
| `ai_assistant.py` | Same chat + file-injection flow as Day 05; uses `CHAT_MODEL` |

Run retrieval demos:

```bash
python day06/test_embedding.py
python day06/test_retriever.py
```

### Day 07 — Planner agent

- `choose_tools()` asks the chat model which of three tools matches the user request (or none).
- `assistant.py` runs the tool in Python, then calls the model again to phrase the reply without mentioning tools.
- See [day07/README.md](day07/README.md) for architecture, examples, and production-style improvements (JSON tool calls, memory, RAG).

## Project layout

```
ai-agent-development/
├── day01/          # Hello AI + basic REPL          → day01/README.md
├── day02/          # Memory + thinking parser        → day02/README.md
├── day03/          # System roles / personalities    → day03/README.md
├── day04/          # Tool functions                  → day04/README.md
├── day05/          # Read files into prompts         → day05/README.md
├── day06/          # Embeddings, similarity, RAG     → day06/README.md
├── day07/          # LLM planner + tool agent        → day07/README.md
├── .env            # Local config (not in git)
└── .personal/      # Personal notes (ignored by git)
```

Each `dayNN/README.md` documents that day’s files, execution flow, and how to run the scripts.

## Configuration notes

- **Timeouts**: Day 01–05 assistants use a 120s client timeout; the thinking assistant uses 180s and higher `max_tokens` for long reasoning outputs.
- **Working directory**: Day 06 `retriever.load_documents()` expects `day06/knowledge` relative to the repo root—run commands from the root.
- **API errors**: Assistants catch `APIError` and generic exceptions so a bad model name or stopped Ollama fails with a clear message.

## License

Learning project—use and adapt as you like.
