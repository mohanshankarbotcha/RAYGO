"""Agent Run Tracker Context Manager.

Provides structured lifecycle recording for specialist agents and services.
Captures start/end timestamps, tool calls, policy evaluations, approval gates,
and correlation IDs to populate the `agent_runs` collection for end-to-end trace auditing.
"""

import datetime
import uuid
from typing import Any

from app.repositories.registry import Repositories


def new_agent_run_id() -> str:
    return f"run_{uuid.uuid4().hex[:10]}"


class AgentRunTracker:
    def __init__(
        self,
        repos: Repositories,
        agent_name: str,
        task_type: str,
        correlation_id: str | None = None,
        parent_run_id: str | None = None,
        input_reference: str | None = None,
    ):
        self.repos = repos
        self.agent_name = agent_name
        self.task_type = task_type
        self.correlation_id = correlation_id or f"corr_{uuid.uuid4().hex[:8]}"
        self.parent_run_id = parent_run_id
        self.input_reference = input_reference
        self.output_reference: str | None = None
        self.agent_run_id = new_agent_run_id()
        self.tool_calls: list[dict[str, Any]] = []
        self.policy_evaluation_id: str | None = None
        self.approval_id: str | None = None
        self.status = "running"
        self.error_code: str | None = None
        self.started_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.completed_at: str | None = None

    def record_tool_call(self, tool_name: str, side_effect: str = "READ_ONLY") -> None:
        self.tool_calls.append(
            {
                "toolName": tool_name,
                "sideEffect": side_effect,
                "recordedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            }
        )

    def link_policy_evaluation(self, policy_evaluation_id: str) -> None:
        self.policy_evaluation_id = policy_evaluation_id

    def link_approval(self, approval_id: str) -> None:
        self.approval_id = approval_id

    def set_output_reference(self, output_reference: str) -> None:
        self.output_reference = output_reference

    async def __aenter__(self) -> "AgentRunTracker":
        record = {
            "id": self.agent_run_id,
            "agentRunId": self.agent_run_id,
            "parentRunId": self.parent_run_id,
            "agentName": self.agent_name,
            "taskType": self.task_type,
            "status": self.status,
            "startedAt": self.started_at,
            "completedAt": None,
            "inputReference": self.input_reference,
            "outputReference": self.output_reference,
            "toolCalls": self.tool_calls,
            "policyEvaluationId": self.policy_evaluation_id,
            "approvalId": self.approval_id,
            "correlationId": self.correlation_id,
            "errorCode": None,
        }
        await self.repos.agent_runs.upsert(record)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        self.completed_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
        if exc_val is not None:
            self.status = "failed"
            self.error_code = getattr(exc_val, "code", exc_type.__name__ if exc_type else "error")
        else:
            self.status = "completed"

        await self.repos.agent_runs.update(
            self.agent_run_id,
            {
                "status": self.status,
                "completedAt": self.completed_at,
                "outputReference": self.output_reference,
                "toolCalls": self.tool_calls,
                "policyEvaluationId": self.policy_evaluation_id,
                "approvalId": self.approval_id,
                "errorCode": self.error_code,
            },
        )
