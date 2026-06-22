#!/usr/bin/env python3
"""Minimal pre-tool safety guard for secret protection and dangerous command blocking."""

import json
import re
import sys
from typing import Any


def _walk_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        out: list[str] = []
        for k, v in value.items():
            out.append(str(k))
            out.extend(_walk_strings(v))
        return out
    if isinstance(value, list):
        out: list[str] = []
        for item in value:
            out.extend(_walk_strings(item))
        return out
    return [str(value)]


def _first_value(obj: Any, keys: list[str]) -> str:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in keys and isinstance(v, str) and v.strip():
                return v
            nested = _first_value(v, keys)
            if nested:
                return nested
    elif isinstance(obj, list):
        for item in obj:
            nested = _first_value(item, keys)
            if nested:
                return nested
    return ""


def _respond(decision: str, reason: str) -> int:
    payload = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
            "permissionDecisionReason": reason,
        }
    }
    print(json.dumps(payload))
    return 0


def main() -> int:
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        return _respond("allow", "Guard failed to parse input; allowing by default.")

    tool_name = _first_value(data, ["toolName", "tool_name", "name", "tool"])
    command_text = _first_value(data, ["command", "input", "query", "args"])

    aggregate_text = "\n".join(_walk_strings(data)).lower()
    check_text = f"{tool_name}\n{command_text}\n{aggregate_text}".lower()

    dangerous_patterns = [
        r"\bgit\s+reset\s+--hard\b",
        r"\bgit\s+checkout\s+--\b",
        r"\brm\s+-rf\s+/(\s|$)",
        r"\bsudo\s+rm\s+-rf\b",
        r"\bmkfs(\.|\s)",
        r"\bdd\s+if=",
        r"\bshutdown\b",
        r"\breboot\b",
    ]
    for pattern in dangerous_patterns:
        if re.search(pattern, check_text):
            return _respond("deny", "Blocked dangerous command pattern by workspace safety guard.")

    secret_exposure_patterns = [
        r"\bcat\s+\.env(\.local)?\b",
        r"\bprintenv\b",
        r"(^|\s)env(\s|$)",
        r"\becho\b.*\b(jira_token|api[_-]?key|secret|password|token)\b",
        r"\b(base64\s*$|\|\s*base64\b)",
        r"\baws\s+configure\s+get\b",
    ]
    for pattern in secret_exposure_patterns:
        if re.search(pattern, check_text):
            return _respond("ask", "Potential secret exposure detected. Confirm before running.")

    return _respond("allow", "No safety rule triggered.")


if __name__ == "__main__":
    raise SystemExit(main())
