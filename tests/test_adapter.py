"""Tests for mcp-protocol-version-adapter."""
import unittest
from mcp_protocol_version_adapter.adapter import MCPProtocolVersionAdapter


class TestProtocolAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = MCPProtocolVersionAdapter()

    def test_adapt_request_args(self):
        req = {"method": "tools/call", "params": {"name": "test", "args": {"x": 1}}}
        adapted = self.adapter.adapt_request(req)
        self.assertEqual(adapted["jsonrpc"], "2.0")
        self.assertIn("arguments", adapted["params"])
        self.assertEqual(adapted["params"]["arguments"]["x"], 1)

    def test_adapt_response_legacy(self):
        res = {"result": {"content": [{"type": "text", "text": "hello"}]}}
        adapted = self.adapter.adapt_response(res, client_legacy=True)
        self.assertEqual(adapted["result"]["text"], "hello")
