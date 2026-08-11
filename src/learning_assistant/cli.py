"""Command-line entry point for stdio and Streamable HTTP MCP transports."""

from __future__ import annotations

import argparse

from learning_assistant.server import mcp


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the learning-assistant MCP server.")
    parser.add_argument(
        "transport",
        nargs="?",
        choices=("stdio", "http"),
        default="stdio",
        help="Use stdio for local clients or http for Streamable HTTP MCP.",
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    if args.transport == "stdio":
        mcp.run("stdio")
    else:
        mcp.run(
            "streamable-http",
            host=args.host,
            port=args.port,
            streamable_http_path="/mcp",
            stateless_http=True,
            json_response=True,
        )


if __name__ == "__main__":
    main()
