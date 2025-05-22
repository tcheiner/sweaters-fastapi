import pytest
from models import Game, User

def test_game_model():
    # Test creating a Game instance
    game = Game(
        gameid="test-game-id",
        userid="1234",
        currRnd=1,
        card_deck={"Hearts": ["A", "2", "3"]}
    )
    
    # Verify attributes
    assert game.gameid == "test-game-id"
    assert game.currRnd == 1
    assert game.userid == "1234"
    assert "Hearts" in game.card_deck
    assert game.card_deck["Hearts"] == ["A", "2", "3"]
    
    # Test JSON serialization
    game_json = game.json()
    assert "gameid" in game_json
    assert "userid" in game_json
    assert "currRnd" in game_json
    assert "card_deck" in game_json

def test_user_model():
    # Test creating a User instance
    user = User(
        userid="test-user-id",
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        games=["game1", "game2"]
    )
    
    # Verify attributes
    assert user.userid == "test-user-id"
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.games == ["game1", "game2"]
    
    # Test JSON serialization
    user_json = user.json()
    assert "userid" in user_json
    assert "username" in user_json
    assert "email" in user_json
    assert "full_name" in user_json
    assert "games" in user_json
