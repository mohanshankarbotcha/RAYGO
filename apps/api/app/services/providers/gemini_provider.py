import asyncio
import json
import logging

from google import genai
from google.genai import types
from pydantic import ValidationError

from app.core.config import Settings
from app.core.errors import (
    GeminiInvalidKeyError,
    GeminiRateLimitError,
    GeminiTimeoutError,
    GeminiUnavailableError,
    StructuredOutputInvalidError,
)
from app.services.providers.base import AgentProvider, SchemaT

logger = logging.getLogger("raygo.gemini")

_SYSTEM_INSTRUCTIONS: dict[str, str] = {
    "coordinator_route": (
        "You are the RAYGO Coordinator. Given a merchant or buyer request, classify its intent and "
        "choose exactly one specialist agent: revenue_intelligence, growth_strategist, experiment_agent, "
        "ai_commerce, policy_guard, or payment_agent. You never execute actions or produce financial "
        "figures yourself — you only route. Respond only with the requested JSON schema."
    ),
    "opportunity_reasoning": (
        "You are the RAYGO Revenue Intelligence agent. You are given a backend-calculated opportunity "
        "record. Explain it in plain language using ONLY the evidence and numbers provided in the "
        "context — never invent financial figures. Respond only with the requested JSON schema."
    ),
    "growth_hypothesis": (
        "You are the RAYGO Growth Strategist agent. Given an approved opportunity and its backend "
        "proposal, write a clear hypothesis. Use only the numbers given in context. You do not execute "
        "anything. Respond only with the requested JSON schema."
    ),
    "experiment_recommendation": (
        "You are the RAYGO Experiment Agent. Given backend-measured control/variant metrics, recommend "
        "SCALE, KEEP_RUNNING, or STOP and explain why using only the given numbers. Respond only with "
        "the requested JSON schema."
    ),
    "commerce_intent": (
        "You are the RAYGO AI Commerce agent. Parse the buyer's natural-language request into a "
        "structured shopping intent (category, budget_max, use_cases). Do not invent product facts — "
        "you are only extracting intent from the buyer's own words. Respond only with the requested "
        "JSON schema."
    ),
}


class GeminiProvider(AgentProvider):
    name = "gemini"

    def __init__(self, settings: Settings):
        self.settings = settings
        # google-genai reads no ambient state here beyond this constructor;
        # the key never leaves this object and is never logged.
        self._client = genai.Client(api_key=settings.gemini_api_key)

    async def generate_structured(self, task: str, context: dict, schema: type[SchemaT]) -> SchemaT:
        system_instruction = _SYSTEM_INSTRUCTIONS.get(task, "Respond only with the requested JSON schema.")
        prompt = (
            f"Task: {task}\n"
            f"Context (authoritative backend data, do not contradict it):\n"
            f"{json.dumps(context, default=str)}\n"
            "Return only the JSON object described by the response schema."
        )

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=self.settings.gemini_temperature,
            response_mime_type="application/json",
            response_schema=schema,
        )

        last_error: Exception | None = None
        for attempt in range(self.settings.gemini_max_retries + 1):
            try:
                response = await asyncio.wait_for(
                    self._client.aio.models.generate_content(
                        model=self.settings.gemini_model,
                        contents=prompt,
                        config=config,
                    ),
                    timeout=self.settings.gemini_timeout_seconds,
                )
                break
            except asyncio.TimeoutError as exc:
                last_error = exc
                logger.warning("Gemini request timed out (attempt %s)", attempt + 1)
                continue
            except Exception as exc:  # noqa: BLE001 - reclassified below
                message = str(exc)
                if "429" in message or "RESOURCE_EXHAUSTED" in message.upper():
                    raise GeminiRateLimitError("Gemini rate limit exceeded.") from exc
                if "401" in message or "403" in message or "API_KEY_INVALID" in message.upper():
                    # Never include the key or raw exception text that might echo it.
                    raise GeminiInvalidKeyError("Gemini rejected the configured API key.") from exc
                last_error = exc
                logger.warning("Gemini request failed (attempt %s): %s", attempt + 1, type(exc).__name__)
                continue
        else:
            if isinstance(last_error, asyncio.TimeoutError):
                raise GeminiTimeoutError("Gemini did not respond within the configured timeout.")
            raise GeminiUnavailableError("Gemini is unavailable after retrying.")

        text = getattr(response, "text", None)
        if not text:
            raise StructuredOutputInvalidError("Gemini returned an empty response.")
        try:
            data = json.loads(text)
            return schema.model_validate(data)
        except (json.JSONDecodeError, ValidationError) as exc:
            raise StructuredOutputInvalidError(
                "Gemini's structured output failed schema validation.", {"task": task}
            ) from exc

    async def health(self) -> dict:
        if not self.settings.gemini_api_key:
            return {"provider": self.name, "configured": False, "status": "missing_key"}
        try:
            await asyncio.wait_for(
                self._client.aio.models.generate_content(
                    model=self.settings.gemini_model,
                    contents="Respond with the single word: ok",
                ),
                timeout=self.settings.gemini_timeout_seconds,
            )
            return {"provider": self.name, "configured": True, "status": "ok"}
        except Exception as exc:  # noqa: BLE001
            message = str(exc)
            if "401" in message or "403" in message or "API_KEY_INVALID" in message.upper():
                return {"provider": self.name, "configured": True, "status": "invalid_key"}
            return {"provider": self.name, "configured": True, "status": "unreachable"}
