"""
LLM service using the OpenAI Responses API.
"""

from openai import OpenAI

from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_repo_answer(
    user_message: str,
    intent: str,
    repo_path: str,
    memory_messages: list[dict],
    tool_result: dict,
) -> str:
    """
    Generate a natural-language assistant answer from tool results and memory.
    """
    memory_text = "\n".join(
        [f'{msg["role"]}: {msg["content"]}' for msg in memory_messages[-6:]]
    )

    prompt = f"""
You are Repo Pilot, an AI engineering workspace assistant.

Your job:
- Answer clearly and simply.
- Base the answer on the tool result and repo context.
- Do not invent files, code, or features not present in the provided data.
- Be practical and helpful for a developer workflow.

User request:
{user_message}

Detected intent:
{intent}

Repository path:
{repo_path}

Recent memory:
{memory_text if memory_text else "No prior memory."}

Tool result:
{tool_result}

Write the final assistant answer.
"""

    response = client.responses.create(
        model=settings.OPENAI_MODEL,
        input=prompt,
    )

    return response.output_text