import uuid

from fastapi import Request

DEMO_MERCHANT_ID = "merchant_novatech"
DEMO_APPROVED_BY = "merchant_demo_user"


def new_request_id() -> str:
    return f"req_{uuid.uuid4().hex[:12]}"


async def request_id_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or new_request_id()
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


def resolve_merchant_id(request: Request, body_merchant_id: str | None = None) -> str:
    """Resolve merchant context for demo purposes.

    Precedence: request body > X-Demo-Merchant-Id header > default demo merchant.
    """
    if body_merchant_id:
        return body_merchant_id
    header_value = request.headers.get("X-Demo-Merchant-Id")
    return header_value or DEMO_MERCHANT_ID
