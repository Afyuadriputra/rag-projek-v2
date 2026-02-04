import os
import time
from typing import Dict, Any

from langchain_openai import ChatOpenAI

PRIMARY_MODEL = os.environ.get(
    "OPENROUTER_MODEL",
    "qwen/qwen3-next-80b-a3b-instruct:free"
)

BACKUP_MODELS_RAW = [
    PRIMARY_MODEL,
    "nvidia/nemotron-3-nano-30b-a3b:free",
    "arcee-ai/trinity-large-preview:free",
    "qwen/qwen3-next-80b-a3b-instruct:free",
    "arcee-ai/trinity-large-preview:free",
    "meta-llama/llama-3.3-70b-instruct:free",
]
BACKUP_MODELS = [m.strip() for m in BACKUP_MODELS_RAW if isinstance(m, str) and m.strip()]

REQUEST_TIMEOUT_SEC = int(os.environ.get("OPENROUTER_TIMEOUT", "45"))
MAX_RETRIES = int(os.environ.get("OPENROUTER_MAX_RETRIES", "1"))
TEMPERATURE = float(os.environ.get("OPENROUTER_TEMPERATURE", "0.2"))


def build_llm(model_name: str) -> ChatOpenAI:
    return ChatOpenAI(
        openai_api_key=os.environ.get("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        model_name=model_name,
        temperature=TEMPERATURE,
        request_timeout=REQUEST_TIMEOUT_SEC,
        max_retries=MAX_RETRIES,
        default_headers={
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "AcademicChatbot",
        },
    )


def invoke_text(llm: ChatOpenAI, prompt: str) -> str:
    out = llm.invoke(prompt)
    if hasattr(out, "content"):
        return out.content or ""
    return str(out)


def llm_fallback_message(last_error: str) -> Dict[str, Any]:
    return {"answer": f"Maaf, semua server AI sedang sibuk. (Error: {last_error})", "sources": []}
