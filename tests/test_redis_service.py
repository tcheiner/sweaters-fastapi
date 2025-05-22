import pytest
from unittest.mock import patch, MagicMock
from services.redis_service import (
    save_user_to_redis, get_user_from_redis, delete_user_from_redis,
    save_game_to_redis, get_game_from_redis, delete_game_from_redis,
    get_all_users_from_redis, get_all_games_from_redis
)

# Test save_user_to_redis function
@pytest.mark.asyncio
@patch('services.redis_service.redis_client')
async def test_save_user_to_redis(mock_redis):
    # Setup mock
    mock_user = MagicMock()
    mock_user.userid = "test-user-id"
    mock_user.json.return_value = '{"userid": "test-user-id"}'
    
    # Call the function
    result = await save_user_to_redis(mock_user)
    
    # Verify the result
    assert result == mock_user
    
    # Verify the redis client was called
    mock_redis.set.assert_called_once_with("user:test-user-id", '{"userid": "test-user-id"}')

# Test get_user_from_redis function
@pytest.mark.asyncio
@patch('services.redis_service.redis_client')
@patch('services.redis_service.User')
async def test_get_user_from_redis(mock_user_class, mock_redis):
    # Setup mocks
    mock_redis.get.return_value = '{"userid": "test-user-id"}'
    mock_user = MagicMock()
    mock_user_class.parse_raw.return_value = mock_user
    
    # Call the function
    result = await get_user_from_redis("test-user-id")
    
    # Verify the result
    assert result == mock_user
    
    # Verify the redis client was called
    mock_redis.get.assert_called_once_with("user:test-user-id")
    mock_user_class.parse_raw.assert_called_once_with('{"userid": "test-user-id"}')

# Test delete_user_from_redis function
@pytest.mark.asyncio
@patch('services.redis_service.redis_client')
async def test_delete_user_from_redis(mock_redis):
    # Setup mock
    mock_redis.delete.return_value = 1
    
    # Call the function
    result = await delete_user_from_redis("test-user-id")
    
    # Verify the result
    assert result == 1
    
    # Verify the redis client was called
    mock_redis.delete.assert_called_once_with("user:test-user-id")

# Test save_game_to_redis function
@pytest.mark.asyncio
@patch('services.redis_service.redis_client')
async def test_save_game_to_redis(mock_redis):
    # Setup mock
    mock_game = MagicMock()
    mock_game.gameid = "test-game-id"
    mock_game.json.return_value = '{"gameid": "test-game-id"}'
    
    # Call the function
    result = await save_game_to_redis(mock_game)
    
    # Verify the result
    assert result == mock_game
    
    # Verify the redis client was called
    mock_redis.set.assert_called_once_with("game:test-game-id", '{"gameid": "test-game-id"}')

# Test get_game_from_redis function
@pytest.mark.asyncio
@patch('services.redis_service.redis_client')
@patch('services.redis_service.Game')
async def test_get_game_from_redis(mock_game_class, mock_redis):
    # Setup mocks
    mock_redis.get.return_value = '{"gameid": "test-game-id"}'
    mock_game = MagicMock()
    mock_game_class.parse_raw.return_value = mock_game
    
    # Call the function
    result = await get_game_from_redis("test-game-id")
    
    # Verify the result
    assert result == mock_game
    
    # Verify the redis client was called
    mock_redis.get.assert_called_once_with("game:test-game-id")
    mock_game_class.parse_raw.assert_called_once_with('{"gameid": "test-game-id"}')

# Test delete_game_from_redis function
@pytest.mark.asyncio
@patch('services.redis_service.redis_client')
async def test_delete_game_from_redis(mock_redis):
    # Setup mock
    mock_redis.delete.return_value = 1
    
    # Call the function
    result = await delete_game_from_redis("test-game-id")
    
    # Verify the result
    assert result == 1
    
    # Verify the redis client was called
    mock_redis.delete.assert_called_once_with("game:test-game-id")

# Test get_all_users_from_redis function
@pytest.mark.asyncio
@patch('services.redis_service.redis_client')
@patch('services.redis_service.User')
async def test_get_all_users_from_redis(mock_user_class, mock_redis):
    # Setup mocks
    mock_redis.keys.return_value = ["user:1", "user:2"]
    mock_redis.get.side_effect = ['{"userid": "1"}', '{"userid": "2"}']
    mock_user1 = MagicMock()
    mock_user2 = MagicMock()
    mock_user_class.parse_raw.side_effect = [mock_user1, mock_user2]
    
    # Call the function
    result = await get_all_users_from_redis()
    
    # Verify the result
    assert len(result) == 2
    assert mock_user1 in result
    assert mock_user2 in result
    
    # Verify the redis client was called
    mock_redis.keys.assert_called_once_with("user:*")
    assert mock_redis.get.call_count == 2
    assert mock_user_class.parse_raw.call_count == 2

# Test get_all_games_from_redis function
@pytest.mark.asyncio
@patch('services.redis_service.redis_client')
@patch('services.redis_service.Game')
async def test_get_all_games_from_redis(mock_game_class, mock_redis):
    # Setup mocks
    mock_redis.keys.return_value = ["game:1", "game:2"]
    mock_redis.get.side_effect = ['{"gameid": "1"}', '{"gameid": "2"}']
    mock_game1 = MagicMock()
    mock_game2 = MagicMock()
    mock_game_class.parse_raw.side_effect = [mock_game1, mock_game2]
    
    # Call the function
    result = await get_all_games_from_redis()
    
    # Verify the result
    assert len(result) == 2
    assert mock_game1 in result
    assert mock_game2 in result
    
    # Verify the redis client was called
    mock_redis.keys.assert_called_once_with("game:*")
    assert mock_redis.get.call_count == 2
    assert mock_game_class.parse_raw.call_count == 2
