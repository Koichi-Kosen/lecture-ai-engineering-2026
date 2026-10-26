from types import SimpleNamespace
from unittest.mock import Mock

from app import ask as ask_module


def test_ask_prints_input_and_output_token_counts(monkeypatch, capsys):
    response = SimpleNamespace(
        usage_metadata=SimpleNamespace(
            prompt_token_count=12,
            candidates_token_count=5,
        ),
        text="回答",
    )
    client = SimpleNamespace(
        models=SimpleNamespace(generate_content=Mock(return_value=response))
    )
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(ask_module.genai, "Client", Mock(return_value=client))

    assert ask_module.ask("質問") == "回答"
    assert capsys.readouterr().out == "[トークン数] 入力: 12, 出力: 5\n"


def test_ask_reports_missing_token_usage(monkeypatch, capsys):
    response = SimpleNamespace(usage_metadata=None, text="回答")
    client = SimpleNamespace(
        models=SimpleNamespace(generate_content=Mock(return_value=response))
    )
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(ask_module.genai, "Client", Mock(return_value=client))

    assert ask_module.ask("質問") == "回答"
    assert capsys.readouterr().out == "[トークン数] 入力・出力トークン数を取得できませんでした\n"
