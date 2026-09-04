import hashlib
import hmac
import uuid

import razorpay

from app.core.config import Settings
from app.core.errors import RazorpayNotConfiguredError, RazorpayOrderFailedError


class RazorpayService:
    """The only backend module allowed to know Razorpay credentials.
    Gemini/ADK/other services must never import this directly."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self._configured = bool(settings.razorpay_key_id and settings.razorpay_key_secret)
        self._client = (
            razorpay.Client(auth=(settings.razorpay_key_id, settings.razorpay_key_secret))
            if self._configured
            else None
        )

    @property
    def configured(self) -> bool:
        return self._configured

    def create_order(self, amount_subunits: int, currency: str, receipt: str) -> dict:
        if self.settings.razorpay_mode != "test":
            raise RazorpayNotConfiguredError("Only Razorpay Test Mode is permitted in this environment.")

        if not self._configured:
            if not self.settings.allow_razorpay_stub:
                raise RazorpayNotConfiguredError(
                    "Razorpay keys are not configured and ALLOW_RAZORPAY_STUB is false.",
                )
            # Local-demo fallback so the judge flow works without live Razorpay
            # Test Mode keys. Clearly marked as a stub order id.
            return {
                "id": f"order_stub_{uuid.uuid4().hex[:12]}",
                "amount": amount_subunits,
                "currency": currency,
                "receipt": receipt,
                "status": "created",
            }

        try:
            return self._client.order.create(
                {
                    "amount": amount_subunits,
                    "currency": currency,
                    "receipt": receipt,
                    "payment_capture": 1,
                }
            )
        except Exception as exc:  # noqa: BLE001 - surfaced as a stable error code
            raise RazorpayOrderFailedError(str(exc)) from exc

    def verify_payment_signature(
        self, razorpay_order_id: str, razorpay_payment_id: str, razorpay_signature: str
    ) -> bool:
        if not self._configured:
            # Stub mode: accept signatures produced by `sign_stub_payment` below
            # so the end-to-end demo flow works without live keys.
            expected = self._stub_signature(razorpay_order_id, razorpay_payment_id)
            return hmac.compare_digest(expected, razorpay_signature)

        try:
            self._client.utility.verify_payment_signature(
                {
                    "razorpay_order_id": razorpay_order_id,
                    "razorpay_payment_id": razorpay_payment_id,
                    "razorpay_signature": razorpay_signature,
                }
            )
            return True
        except razorpay.errors.SignatureVerificationError:
            return False

    def verify_webhook_signature(self, raw_body: bytes, signature: str) -> bool:
        secret = self.settings.razorpay_webhook_secret
        if not secret:
            return self.settings.allow_razorpay_stub
        expected = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)

    def _stub_signature(self, razorpay_order_id: str, razorpay_payment_id: str) -> str:
        secret = self.settings.razorpay_key_secret or "raygo_local_stub_secret"
        payload = f"{razorpay_order_id}|{razorpay_payment_id}".encode("utf-8")
        return hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()

    def sign_stub_payment(self, razorpay_order_id: str, razorpay_payment_id: str) -> str:
        """Test helper: produces a signature that `verify_payment_signature`
        will accept when running without real Razorpay keys."""
        return self._stub_signature(razorpay_order_id, razorpay_payment_id)
