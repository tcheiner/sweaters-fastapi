import pytest
from unittest.mock import patch, MagicMock
from services.user_service import create_user, get_user, add_game_to_user
from models import  User

# Test create_user function
@pytest.mark.asyncio
@patch('services.user_service.save_user_to_redis')
async def test_create_user(mock_save_user):
    # Setup mock
    mock_save_user.return_value = None  # Mock the save_user_to_redis function

    # Define expected user
    expected_user = User(
        userid="some-generated-id",  # Replace with the actual ID generation logic if needed
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        games=[]
    )

    # Call the function
    result = await create_user("testuser", "test@example.com", "Test User")

    # Verify the result
    assert result.username == expected_user.username
    assert result.email == expected_user.email
    assert result.full_name == expected_user.full_name
    assert result.games == expected_user.games

    # Verify the mock was called with the correct arguments
    mock_save_user.assert_called_once_with(result)

# Test get_user function
@pytest.mark.asyncio
@patch('services.user_service.get_user_from_redis')
async def test_get_user(mock_get_user):
    # Setup mock
    mock_user = MagicMock()
    mock_get_user.return_value = mock_user
    
    # Call the function
    result = await get_user("test-user-id")
    
    # Verify the result
    assert result == mock_user
    
    # Verify the mock was called with correct parameters
    mock_get_user.assert_called_once_with("test-user-id")

# Test add_game_to_user function for guest user
@pytest.mark.asyncio
async def test_add_game_to_guest_user():
    # Call the function with guest user
    result = await add_game_to_user("guest", "test-game-id")
    
    # Verify the result
    assert result["userid"] == "guest"
    assert "test-game-id" in result["games"]

# Test add_game_to_user function for existing user
@pytest.mark.asyncio
@patch('services.user_service.get_user')
@patch('services.user_service.save_user_to_redis')
async def test_add_game_to_existing_user(mock_save_user, mock_get_user):
    # Setup mocks
    mock_user = MagicMock()
    mock_user.games = []
    mock_get_user.return_value = mock_user
    mock_save_user.return_value = mock_user
    
    # Call the function
    result = await add_game_to_user("test-user-id", "test-game-id")
    
    # Verify the result
    assert result == mock_user
    
    # Verify the game was added to the user's games
    assert "test-game-id" in mock_user.games
    
    # Verify the mocks were called
    mock_get_user.assert_called_once_with("test-user-id")
    mock_save_user.assert_called_once_with(mock_user)

# Test add_game_to_user function for non-existent user
@pytest.mark.asyncio
@patch('services.user_service.get_user')
@patch('services.user_service.save_user_to_redis')
async def test_add_game_to_nonexistent_user(mock_save_user, mock_get_user):
    # Setup mocks
    mock_get_user.return_value = None
    mock_save_user.return_value = MagicMock()
    
    # Call the function
    result = await add_game_to_user("new-user-id", "test-game-id")
    
    # Verify the mocks were called
    mock_get_user.assert_called_once_with("new-user-id")
    mock_save_user.assert_called_once()
    
    # Verify a new user was created with the game
    call_args = mock_save_user.call_args[0][0]
    assert call_args.userid == "new-user-id"
    assert "test-game-id" in call_args.games
