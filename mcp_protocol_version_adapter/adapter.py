"""Core MCP Protocol Version Adapter implementation."""
import json
from typing import Dict, Any


class MCPProtocolVersionAdapter:
    def __init__(self, target_version: str = "2026-03-01"):
        self.target_version = target_version

    def adapt_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        req_copy = dict(request)
        # Ensure jsonrpc version
        req_copy["jsonrpc"] = "2.0"

        # Adapt legacy tool calling format
        if req_copy.get("method") == "tools/call":
            params = req_copy.get("params", {})
            # If arguments are passed under legacy key 'args', map to 'arguments'
            if "args" in params and "arguments" not in params:
                params["arguments"] = params.pop("args")
            req_copy["params"] = params

        return req_copy

    def adapt_response(self, response: Dict[str, Any], client_legacy: bool = False) -> Dict[str, Any]:
        res_copy = dict(response)
        res_copy["jsonrpc"] = "2.0"

        if client_legacy and "result" in res_copy:
            # Map modern content array to legacy flat text if required
            result = res_copy["result"]
            if isinstance(result, dict) and "content" in result:
                contents = result["content"]
                if isinstance(contents, list) and len(contents) > 0:
                    first = contents[0]
                    if isinstance(first, dict) and "text" in first:
                        result["text"] = first["text"]

        return res_copy
