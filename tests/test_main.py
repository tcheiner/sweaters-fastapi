import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from models import User
from main import app

client = TestClient(app)

# Test create_user_endpoint
@patch('main.create_user')
def test_create_user_endpoint(mock_create_user):
    # Create a mock User object
    mock_user = User(
        userid="12345",
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        games=[]
    )
    mock_create_user.return_value = mock_user  # Mock the return value of create_user

    # Make the request
    response = client.post("/users/?username=testuser&email=test@example.com&full_name=Test+User")

    # Verify the response
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User created successfully"
    assert data["user"]["username"] == "testuser"
    assert data["user"]["email"] == "test@example.com"
    assert data["user"]["full_name"] == "Test User"
# Test get_user_endpoint
@patch('main.get_user')
def test_get_user_endpoint_success(mock_get_user):
    # Setup mock
    mock_user = MagicMock()
    mock_get_user.return_value = mock_user
    
    # Make the request
    response = client.get("/users/test-id")
    
    # Verify the response
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status_code"] == 200
    assert json_response["message"] == "User retrieved successfully"
    assert "user" in json_response
    
    # Verify the mock was called
    mock_get_user.assert_called_once_with("test-id")

@patch('main.get_user')
def test_get_user_endpoint_not_found(mock_get_user):
    # Setup mock
    mock_get_user.return_value = None
    
    # Make the request
    response = client.get("/users/nonexistent-id")
    
    # Verify the response
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
    
    # Verify the mock was called
    mock_get_user.assert_called_once_with("nonexistent-id")

# Test add_game_to_user_endpoint
@patch('main.add_game_to_user')
def test_add_game_to_user_endpoint_success(mock_add_game):
    # Setup mock
    mock_user = MagicMock()
    mock_add_game.return_value = mock_user
    
    # Make the request
    response = client.post("/users/test-id/games/?gameid=test-game-id")
    
    # Verify the response
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status_code"] == 200
    assert json_response["message"] == "Game added to user successfully"
    assert "user" in json_response
    
    # Verify the mock was called
    mock_add_game.assert_called_once_with("test-id", "test-game-id")

@patch('main.add_game_to_user')
def test_add_game_to_user_endpoint_not_found(mock_add_game):
    # Setup mock
    mock_add_game.return_value = None
    
    # Make the request
    response = client.post("/users/nonexistent-id/games/?gameid=test-game-id")
    
    # Verify the response
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
    
    # Verify the mock was called
    mock_add_game.assert_called_once_with("nonexistent-id", "test-game-id")

# Test start_game_endpoint
@patch('main.start_game')
def test_start_game_endpoint(mock_start_game):
    # Setup mock
    mock_start_game.return_value = {"message": "Game started", "game_id": "test-game-id", "user_id": "test-user-id"}
    
    # Make the request
    response = client.get("/start-game?userid=test-user-id")
    
    # Verify the response
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status_code"] == 200
    assert json_response["message"] == "Game started"
    assert json_response["data"]["game_id"] == "test-game-id"
    assert json_response["data"]["user_id"] == "test-user-id"
    
    # Verify the mock was called
    mock_start_game.assert_called_once_with("test-user-id")

# Test reset_game_endpoint
@patch('main.reset_game')
def test_reset_game_endpoint(mock_reset_game):
    # Setup mock
    mock_reset_game.return_value = {"message": "Game reset", "game_id": "test-game-id", "user_id": "test-user-id"}
    
    # Make the request
    response = client.post("/reset-game?gameid=test-game-id&userid=test-user-id")
    
    # Verify the response
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status_code"] == 200
    assert json_response["message"] == "Game reset"
    assert json_response["data"]["game_id"] == "test-game-id"
    assert json_response["data"]["user_id"] == "test-user-id"
    
    # Verify the mock was called
    mock_reset_game.assert_called_once_with("test-game-id", "test-user-id")

# Test list_users_endpoint
@patch('main.get_all_users_from_redis')
def test_list_users_endpoint(mock_get_all_users):
    # Setup mock
    mock_user1 = MagicMock()
    mock_user2 = MagicMock()
    mock_get_all_users.return_value = [mock_user1, mock_user2]
    
    # Make the request
    response = client.get("/users")
    
    # Verify the response
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status_code"] == 200
    assert json_response["message"] == "Users retrieved successfully"
    assert "users" in json_response["data"]
    
    # Verify the mock was called
    mock_get_all_users.assert_called_once()

# Test list_games_endpoint
@patch('main.get_all_games_from_redis')
def test_list_games_endpoint(mock_get_all_games):
    # Setup mock
    mock_game1 = MagicMock()
    mock_game2 = MagicMock()
    mock_get_all_games.return_value = [mock_game1, mock_game2]
    
    # Make the request
    response = client.get("/games")
    
    # Verify the response
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status_code"] == 200
    assert json_response["message"] == "Games retrieved successfully"
    assert "games" in json_response["data"]
    
    # Verify the mock was called
    mock_get_all_games.assert_called_once()

# Test pull_card_endpoint success
@patch('main.pull_card')
@patch('main.get_game_from_redis')
@patch('main.get_user')
def test_pull_card_endpoint_success(mock_get_user, mock_get_game, mock_pull_card):
    # Setup mocks
    mock_pull_card.return_value = {
        "message": "Card pulled successfully",
        "game_id": "test-game-id",
        "user_id": "test-user-id",
        "round": 1,
        "cards": {"Hearts": "A", "Diamonds": "K"}
    }
    mock_game = MagicMock()
    mock_get_game.return_value = mock_game
    mock_user = MagicMock()
    mock_get_user.return_value = mock_user
    
    # Make the request
    response = client.get("/pull-card?userid=test-user-id&gameid=test-game-id")
    
    # Verify the response
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status_code"] == 200
    assert json_response["message"] == "Card pulled successfully"
    assert json_response["game"] is not None
    assert json_response["user"] is not None
    assert json_response["data"]["cards"]["Hearts"] == "A"
    assert json_response["data"]["cards"]["Diamonds"] == "K"
    
    # Verify the mocks were called
    mock_pull_card.assert_called_once_with("test-user-id", "test-game-id")
    mock_get_game.assert_called_once_with("test-game-id")
    mock_get_user.assert_called_once_with("test-user-id")

# Test pull_card_endpoint error
@patch('main.pull_card')
def test_pull_card_endpoint_error(mock_pull_card):
    # Setup mock
    mock_pull_card.return_value = {
        "error": "Game not found",
        "game_id": "nonexistent-id"
    }
    
    # Make the request
    response = client.get("/pull-card?userid=test-user-id&gameid=nonexistent-id")
    
    # Verify the response
    assert response.status_code == 200  # API returns 200 with error in body
    json_response = response.json()
    assert json_response["status_code"] == 400  # Status code in body is 400
    assert json_response["message"] == "Game not found"
    assert "data" in json_response
    
    # Verify the mock was called
    mock_pull_card.assert_called_once_with("test-user-id", "nonexistent-id")
