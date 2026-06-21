from app.main import main


def test_worker_entrypoint_is_callable() -> None:
    assert callable(main)
