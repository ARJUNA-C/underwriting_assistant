import os
import json
import logging
from typing import Type, TypeVar
from pydantic import BaseModel, ValidationError
import httpx
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

class LLMError(Exception):
    """Base exception for LLM call failures."""
    pass

class LLMValidationError(LLMError):
    """Raised when LLM output fails schema validation after retries."""
    pass

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = "openai/gpt-oss-120b"

async def call_groq_json(
    system_prompt: str,
    user_prompt: str,
    target_schema: Type[T],
    model: str = DEFAULT_MODEL,
    temperature: float = 0.1,
) -> T:
    """
    Calls Groq API with JSON mode enabled, validating response against `target_schema`.
    Retries once on Pydantic validation failure.
    """
    api_key = os.getenv("GROQ_API_KEY", GROQ_API_KEY)
    if not api_key:
        raise LLMError("GROQ_API_KEY is not set in environment or .env file.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    async with httpx.AsyncClient(timeout=60.0) as client:
        last_error = None
        for attempt in range(2):  # First pass + 1 retry
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "response_format": {"type": "json_object"},
            }

            try:
                response = await client.post(GROQ_API_URL, headers=headers, json=payload)
                if response.status_code != 200:
                    error_msg = f"Groq API HTTP error {response.status_code}: {response.text}"
                    logger.error(error_msg)
                    raise LLMError(error_msg)

                res_json = response.json()
                content = res_json["choices"][0]["message"]["content"]

                # Validate against target_schema
                parsed_obj = target_schema.model_validate_json(content)
                return parsed_obj

            except (json.JSONDecodeError, ValidationError) as e:
                last_error = str(e)
                logger.warning(f"Attempt {attempt + 1} validation failed for {target_schema.__name__}: {last_error}")
                if attempt == 0:
                    # Append feedback for 1-retry policy
                    messages.append({"role": "assistant", "content": content if 'content' in locals() else ""})
                    messages.append({
                        "role": "user",
                        "content": f"Your previous response failed validation: {last_error}. Fix and resend valid JSON matching the schema exactly."
                    })
                else:
                    raise LLMValidationError(
                        f"Failed to produce valid JSON for {target_schema.__name__} after retry: {last_error}"
                    ) from e
            except Exception as e:
                if isinstance(e, (LLMError, LLMValidationError)):
                    raise e
                raise LLMError(f"Unexpected error calling Groq API: {str(e)}") from e

    raise LLMValidationError(f"Failed schema validation for {target_schema.__name__}: {last_error}")
