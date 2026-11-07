from ghostbus.runtime import APP_IMPORT, DEFAULT_HOST, DEFAULT_PORT, main, parse_args, run


def test_run_starts_uvicorn_with_the_asgi_app(monkeypatch) -> None:
    calls: list[tuple[tuple, dict]] = []

    def fake_run(*args, **kwargs) -> None:
        calls.append((args, kwargs))

    monkeypatch.setattr("ghostbus.runtime.uvicorn.run", fake_run)
    run()

    assert calls == [
        (
            (APP_IMPORT,),
            {"host": DEFAULT_HOST, "port": DEFAULT_PORT},
        )
    ]
    assert APP_IMPORT == "ghostbus.server:app"


def test_parse_args_defaults_to_8000() -> None:
    assert parse_args([]).port == DEFAULT_PORT


def test_parse_args_reads_port() -> None:
    assert parse_args(["--port", "9000"]).port == 9000


def test_main_starts_on_given_port(monkeypatch) -> None:
    calls: list[dict] = []

    def fake_run(*args, **kwargs) -> None:
        calls.append(kwargs)

    monkeypatch.setattr("ghostbus.runtime.uvicorn.run", fake_run)
    main(["--port", "9000"])

    assert calls == [{"host": DEFAULT_HOST, "port": 9000}]
