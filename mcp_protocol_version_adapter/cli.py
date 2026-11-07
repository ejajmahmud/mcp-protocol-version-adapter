"""CLI for mcp-protocol-version-adapter."""
import sys
import argparse
from .adapter import MCPProtocolVersionAdapter


def main():
    parser = argparse.ArgumentParser(description="MCP Protocol Version Adapter")
    parser.add_argument("--demo", action="store_true", help="Run demonstration")
    args = parser.parse_args()

    if args.demo:
        adapter = MCPProtocolVersionAdapter()
        legacy_req = {
            "method": "tools/call",
            "params": {"name": "query_db", "args": {"limit": 10}}
        }
        adapted = adapter.adapt_request(legacy_req)
        print(f"Original: {legacy_req}")
        print(f"Adapted: {adapted}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
