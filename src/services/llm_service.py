import json
import logging
import time
from pathlib import Path
from typing import Type

import anthropic
from pydantic import BaseModel

from src.config import settings

logger = logging.getLogger(__name__)

PROMPT_DIR = Path(__file__).parent.parent / "prompts"


class LLMService:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.llm_model

    def _load_prompt(self, template_name: str, variables: dict) -> tuple[str, str]:
        """Load prompt template and fill variables. Returns (system, user) messages."""
        path = PROMPT_DIR / template_name
        content = path.read_text(encoding="utf-8")

        # Split by "# User" marker
        parts = content.split("# User", 1)
        system_part = parts[0].strip()
        user_part = parts[1].strip() if len(parts) > 1 else ""

        # Remove leading "# System\n" if present
        if system_part.startswith("# System"):
            system_part = system_part[len("# System"):].strip()

        # Fill variables
        for key, value in variables.items():
            system_part = system_part.replace(f"{{{key}}}", str(value))
            user_part = user_part.replace(f"{{{key}}}", str(value))

        return system_part, user_part

    def generate(
        self,
        template_name: str,
        variables: dict,
        response_model: Type[BaseModel] | None = None,
        max_retries: int | None = None,
    ) -> dict:
        """Load template, call LLM, parse JSON response."""
        if max_retries is None:
            max_retries = settings.llm_max_retries

        system_msg, user_msg = self._load_prompt(template_name, variables)

        last_error = None
        for attempt in range(max_retries):
            try:
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=8192,
                    system=system_msg,
                    messages=[{"role": "user", "content": user_msg}],
                )

                text = response.content[0].text

                # Extract JSON from response (handle markdown code blocks)
                text = text.strip()
                if text.startswith("```"):
                    # Remove markdown code block
                    lines = text.split("\n")
                    lines = lines[1:]  # remove opening ```json or ```
                    if lines and lines[-1].strip() == "```":
                        lines = lines[:-1]
                    text = "\n".join(lines)

                result = json.loads(text)

                # Validate with Pydantic if model provided
                if response_model:
                    if isinstance(result, list):
                        [response_model.model_validate(item) for item in result]
                    else:
                        response_model.model_validate(result)

                return result

            except json.JSONDecodeError as e:
                last_error = e
                logger.warning(f"JSON parse error on attempt {attempt + 1}: {e}")
                # Add hint to user message for retry
                user_msg += "\n\n請嚴格遵循 JSON schema，只回傳 JSON，不要有其他文字。"
            except anthropic.APIError as e:
                last_error = e
                logger.warning(f"API error on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    wait = 2 ** (attempt + 1)
                    time.sleep(wait)
            except Exception as e:
                last_error = e
                logger.warning(f"Unexpected error on attempt {attempt + 1}: {e}")

        raise RuntimeError(f"LLM generation failed after {max_retries} attempts: {last_error}")


# Singleton
llm_service = LLMService()
