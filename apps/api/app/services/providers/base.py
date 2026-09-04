from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel

SchemaT = TypeVar("SchemaT", bound=BaseModel)


class AgentProvider(ABC):
    """Everything above this abstraction must not know or care whether
    Gemini or the deterministic fallback produced a result — only that it
    got back a schema-validated object and a `mode` label to surface in the
    UI/audit trail."""

    name: str

    @abstractmethod
    async def generate_structured(self, task: str, context: dict, schema: type[SchemaT]) -> SchemaT:
        """Produce output for `task` validated against `schema`.

        Implementations must never execute a tool themselves — they only
        return structured content. Raises a RaygoError subclass
        (GeminiTimeoutError, GeminiRateLimitError, GeminiInvalidKeyError,
        StructuredOutputInvalidError, ...) on any failure so the caller can
        fall back.
        """
        raise NotImplementedError

    @abstractmethod
    async def health(self) -> dict:
        raise NotImplementedError
