from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


class RaygoError(Exception):
    """Base application error mapped to the stable error envelope."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    code: str = "INTERNAL_ERROR"

    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ValidationErrorX(RaygoError):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "VALIDATION_ERROR"


class NotFoundError(RaygoError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "NOT_FOUND"


class InvalidStateTransitionError(RaygoError):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "INVALID_STATE_TRANSITION"


class PolicyBlockedError(RaygoError):
    status_code = status.HTTP_403_FORBIDDEN
    code = "POLICY_BLOCKED"


class ApprovalRequiredError(RaygoError):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "APPROVAL_REQUIRED"


class IdempotencyConflictError(RaygoError):
    status_code = status.HTTP_409_CONFLICT
    code = "IDEMPOTENCY_CONFLICT"


class InsufficientInventoryError(RaygoError):
    status_code = status.HTTP_409_CONFLICT
    code = "INSUFFICIENT_INVENTORY"



class RazorpayNotConfiguredError(RaygoError):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    code = "RAZORPAY_NOT_CONFIGURED"


class RazorpayOrderFailedError(RaygoError):
    status_code = status.HTTP_502_BAD_GATEWAY
    code = "RAZORPAY_ORDER_FAILED"


class RazorpaySignatureInvalidError(RaygoError):
    status_code = status.HTTP_403_FORBIDDEN
    code = "RAZORPAY_SIGNATURE_INVALID"


class WebhookSignatureInvalidError(RaygoError):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "WEBHOOK_SIGNATURE_INVALID"


class WebhookEventConflictError(RaygoError):
    status_code = status.HTTP_409_CONFLICT
    code = "WEBHOOK_EVENT_CONFLICT"


class DatabaseUnavailableError(RaygoError):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    code = "DATABASE_UNAVAILABLE"


class GeminiNotConfiguredError(RaygoError):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    code = "GEMINI_NOT_CONFIGURED"


class GeminiInvalidKeyError(RaygoError):
    status_code = status.HTTP_502_BAD_GATEWAY
    code = "GEMINI_INVALID_KEY"


class GeminiTimeoutError(RaygoError):
    status_code = status.HTTP_504_GATEWAY_TIMEOUT
    code = "GEMINI_TIMEOUT"


class GeminiRateLimitError(RaygoError):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    code = "GEMINI_RATE_LIMIT"


class GeminiUnavailableError(RaygoError):
    status_code = status.HTTP_502_BAD_GATEWAY
    code = "GEMINI_UNAVAILABLE"


class StructuredOutputInvalidError(RaygoError):
    status_code = status.HTTP_502_BAD_GATEWAY
    code = "STRUCTURED_OUTPUT_INVALID"


class ToolNotAllowedError(RaygoError):
    status_code = status.HTTP_403_FORBIDDEN
    code = "TOOL_NOT_ALLOWED"


def _envelope(code: str, message: str, details: dict, request_id: str) -> dict:
    return {
        "error": {
            "code": code,
            "message": message,
            "details": details,
            "requestId": request_id,
        }
    }


def register_exception_handlers(app) -> None:
    @app.exception_handler(RaygoError)
    async def raygo_error_handler(request: Request, exc: RaygoError):
        request_id = getattr(request.state, "request_id", "req_unknown")
        return JSONResponse(
            status_code=exc.status_code,
            content=_envelope(exc.code, exc.message, exc.details, request_id),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        request_id = getattr(request.state, "request_id", "req_unknown")
        return JSONResponse(
            status_code=422,
            content=_envelope(
                "VALIDATION_ERROR",
                "Request validation failed.",
                {"errors": exc.errors()},
                request_id,
            ),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        request_id = getattr(request.state, "request_id", "req_unknown")
        return JSONResponse(
            status_code=exc.status_code,
            content=_envelope("NOT_FOUND" if exc.status_code == 404 else "INTERNAL_ERROR", str(exc.detail), {}, request_id),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        request_id = getattr(request.state, "request_id", "req_unknown")
        return JSONResponse(
            status_code=500,
            content=_envelope("INTERNAL_ERROR", "An unexpected error occurred.", {}, request_id),
        )
