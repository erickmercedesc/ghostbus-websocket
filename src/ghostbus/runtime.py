import uvicorn

APP_IMPORT = "ghostbus.server:app"
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000


def run(*, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    uvicorn.run(APP_IMPORT, host=host, port=port)
