import argparse

import uvicorn

APP_IMPORT = "ghostbus.server:app"
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="websocket_engine")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    return parser.parse_args(argv)


def run(*, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    uvicorn.run(APP_IMPORT, host=host, port=port)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    run(port=args.port)
