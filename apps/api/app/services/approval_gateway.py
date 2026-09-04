import uuid

from app.core.errors import RaygoError
from app.repositories.base import utcnow_iso
from app.repositories.registry import Repositories

# MVP has no session/auth layer (see docs/MANUAL_TEST_PLAN.md -> Known Gaps).
# This allow-list is a deliberately lightweight stand-in: it is NOT a
# substitute for real authentication, but it does mean an arbitrary or
# AI-supplied `approvedBy` value cannot silently pass as a merchant
# approval -- only names on this list can approve/reject anything.
ALLOWED_APPROVERS = {"merchant_demo_user"}


class UnauthorizedApproverError(RaygoError):
    status_code = 403
    code = "UNAUTHORIZED_APPROVER"


def new_approval_id() -> str:
    return f"appr_{uuid.uuid4().hex[:8]}"


class ApprovalGateway:
    """Approval must always be a separate persisted record tied to a
    policy evaluation. Never inferred from an agent recommendation."""

    def __init__(self, repos: Repositories):
        self.repos = repos

    def _check_authorized(self, approved_by: str) -> None:
        if approved_by not in ALLOWED_APPROVERS:
            raise UnauthorizedApproverError(
                "This approver is not authorized to approve or reject RAYGO actions.",
                {"approvedBy": approved_by},
            )

    async def record_approval(
        self,
        merchant_id: str,
        policy_evaluation_id: str,
        target_type: str,
        target_id: str,
        approved_by: str = "merchant_demo_user",
    ) -> dict:
        self._check_authorized(approved_by)
        now = utcnow_iso()
        approval = {
            "id": new_approval_id(),
            "merchantId": merchant_id,
            "policyEvaluationId": policy_evaluation_id,
            "targetType": target_type,
            "targetId": target_id,
            "status": "approved",
            "approvedBy": approved_by,
            "approvedAt": now,
            "metadata": {},
        }
        return await self.repos.approvals.upsert(approval)

    async def record_rejection(
        self,
        merchant_id: str,
        policy_evaluation_id: str,
        target_type: str,
        target_id: str,
        rejected_by: str = "merchant_demo_user",
        reason: str = "Merchant declined the recommendation.",
    ) -> dict:
        self._check_authorized(rejected_by)
        now = utcnow_iso()
        approval = {
            "id": new_approval_id(),
            "merchantId": merchant_id,
            "policyEvaluationId": policy_evaluation_id,
            "targetType": target_type,
            "targetId": target_id,
            "status": "rejected",
            "approvedBy": rejected_by,
            "approvedAt": now,
            "metadata": {"reason": reason},
        }
        return await self.repos.approvals.upsert(approval)
