from ghostbus.runtime import APP_IMPORT, DEFAULT_HOST, DEFAULT_PORT, run


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
