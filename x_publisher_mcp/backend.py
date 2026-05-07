"""Backends for curated X operations."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any

from .config import Config


@dataclass(frozen=True)
class OperationPlan:
    operation_id: str
    payload: dict[str, Any]
    summary: str
    mutating: bool = True
    category: str = "general"

    def to_dict(self) -> dict[str, Any]:
        return {
            "operation_id": self.operation_id,
            "payload": self.payload,
            "summary": self.summary,
            "mutating": self.mutating,
            "category": self.category,
        }


class Backend:
    def execute(self, plan: OperationPlan) -> dict[str, Any]:
        raise NotImplementedError


class DryRunBackend(Backend):
    def execute(self, plan: OperationPlan) -> dict[str, Any]:
        if not plan.mutating:
            return {
                "status": "backend_not_configured",
                "message": "Read operations need a live official XMCP backend. Set X_PUBLISHER_MODE=live, X_PUBLISHER_ALLOW_LIVE=1, and X_PUBLISHER_XMCP_URL.",
                "plan": plan.to_dict(),
            }
        return {
            "status": "dry_run",
            "message": "Dry-run mode: no request was sent to X.",
            "plan": plan.to_dict(),
        }


class XmcpBackend(Backend):
    def __init__(self, xmcp_url: str):
        self.xmcp_url = xmcp_url

    def execute(self, plan: OperationPlan) -> dict[str, Any]:
        try:
            return asyncio.run(self._execute_async(plan))
        except RuntimeError as exc:
            return {
                "status": "backend_error",
                "message": f"Could not call official XMCP from this runtime: {exc}",
                "plan": plan.to_dict(),
            }

    async def _execute_async(self, plan: OperationPlan) -> dict[str, Any]:
        try:
            from fastmcp import Client
        except ImportError:
            return {
                "status": "backend_not_configured",
                "message": "Install FastMCP dependencies with `python -m pip install -r requirements.txt` before using live XMCP calls.",
                "plan": plan.to_dict(),
            }
        async with Client(self.xmcp_url) as client:
            result = await client.call_tool(plan.operation_id, plan.payload)
        return {
            "status": "ok",
            "message": "Operation executed through official XMCP.",
            "plan": plan.to_dict(),
            "result": _jsonable(result),
        }


class RecordingBackend(Backend):
    def __init__(self):
        self.calls: list[OperationPlan] = []

    def execute(self, plan: OperationPlan) -> dict[str, Any]:
        self.calls.append(plan)
        return {
            "status": "ok",
            "message": "Recorded operation.",
            "plan": plan.to_dict(),
            "result": {"recorded": True},
        }


def backend_from_config(config: Config) -> Backend:
    if config.live_enabled and config.xmcp_url:
        return XmcpBackend(config.xmcp_url)
    return DryRunBackend()


def _jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if hasattr(value, "model_dump"):
        return _jsonable(value.model_dump())
    if hasattr(value, "dict"):
        return _jsonable(value.dict())
    return repr(value)
