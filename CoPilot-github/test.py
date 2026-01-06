# python
import pytest
import learnCopilot
from learnCopilot import (
    determine_winner,
    get_computer_choice,
    get_user_choice,
    play_again,
    play_game,
)

def test_determine_winner_tie():
    assert determine_winner("rock", "rock") == "It's a tie!"
    assert determine_winner("paper", "paper") == "It's a tie!"
    assert determine_winner("scissors", "scissors") == "It's a tie!"

def test_determine_winner_user_win_cases():
    assert determine_winner("rock", "scissors") == "You win!"
    assert determine_winner("paper", "rock") == "You win!"
    assert determine_winner("scissors", "paper") == "You win!"

def test_determine_winner_user_lose_cases():
    assert determine_winner("rock", "paper") == "You lose!"
    assert determine_winner("paper", "scissors") == "You lose!"
    assert determine_winner("scissors", "rock") == "You lose!"

def test_get_computer_choice_returns_valid(monkeypatch):
    monkeypatch.setattr(learnCopilot.random, "choice", lambda seq: "paper")
    assert get_computer_choice() == "paper"

def test_get_user_choice_single_valid(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt="": "Rock")
    assert get_user_choice() == "rock"

def test_get_user_choice_invalid_then_valid(monkeypatch):
    inputs = iter(["invalid", "Scissors"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    assert get_user_choice() == "scissors"

def test_play_again_yes(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt="": "Yes")
    assert play_again() is True

def test_play_again_invalid_then_no(monkeypatch):
    inputs = iter(["maybe", "no"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    assert play_again() is False

def test_play_game_prints_result(monkeypatch, capsys):
    monkeypatch.setattr(learnCopilot, "get_user_choice", lambda: "rock")
    monkeypatch.setattr(learnCopilot, "get_computer_choice", lambda: "scissors")
    play_game()
    captured = capsys.readouterr()
    assert "You chose: rock" in captured.out
    assert "Computer chose: scissors" in captured.out
    assert "You win!" in captured.out