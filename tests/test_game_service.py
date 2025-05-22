import pytest
from unittest.mock import patch, MagicMock
from services.game_service import DeckCards, start_game, reset_game, pull_card

# Test the DeckCards class
def test_deck_cards_init():
    # Test with default suits
    deck = DeckCards()
    assert deck.suits == ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    
    # Test with custom suits
    custom_suits = ['Red', 'Blue']
    deck = DeckCards(custom_suits)
    assert deck.suits == custom_suits

def test_deck_cards_shuffle():
    deck = DeckCards()
    # Create a test array
    test_array = ['A', '2', '3', '4', '5']
    # Shuffle with a fixed seed for reproducibility
    import random
    random.seed(42)
    shuffled = deck.shuffle(test_array[:])
    # Verify the array was shuffled (order changed)
    assert shuffled != ['A', '2', '3', '4', '5']
    # Verify all elements are still present
    assert sorted(shuffled) == sorted(['A', '2', '3', '4', '5'])

def test_deck_cards_initialize_deck():
    deck = DeckCards(['Hearts', 'Diamonds'])
    card_deck = deck.initialize_deck()
    
    # Verify the structure of the deck
    assert 'Hearts' in card_deck
    assert 'Diamonds' in card_deck
    
    # Verify each suit has all 13 cards
    assert len(card_deck['Hearts']) == 13
    assert len(card_deck['Diamonds']) == 13
    
    # Verify all cards are present in each suit
    expected_cards = set(['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'])
    assert set(card_deck['Hearts']) == expected_cards
    assert set(card_deck['Diamonds']) == expected_cards

# Test the start_game function
@pytest.mark.asyncio
@patch('services.game_service.save_game_to_redis')
@patch('services.user_service.add_game_to_user')
async def test_start_game(mock_add_game, mock_save_game):
    # Setup mocks
    mock_save_game.return_value = None
    mock_add_game.return_value = {"userid": "test-user", "games": ["test-game-id"]}
    
    # Call the function
    result = await start_game("test-user")
    
    # Verify the result
    assert "message" in result
    assert "game_id" in result
    assert "user_id" in result
    assert result["user_id"] == "test-user"
    
    # Verify the mocks were called
    mock_save_game.assert_called_once()
    mock_add_game.assert_called_once()

# Test the reset_game function
@pytest.mark.asyncio
@patch('services.game_service.get_game_from_redis')
@patch('services.game_service.save_game_to_redis')
async def test_reset_game_existing(mock_save_game, mock_get_game):
    # Setup mock for existing game
    mock_game = MagicMock()
    mock_game.gameid = "test-game-id"
    mock_get_game.return_value = mock_game
    
    # Call the function
    result = await reset_game("test-game-id", "test-user")
    
    # Verify the result
    assert "message" in result
    assert "game_id" in result
    assert result["game_id"] == "test-game-id"
    assert "user_id" in result
    assert result["user_id"] == "test-user"
    
    # Verify the game was updated
    assert mock_game.currRnd == 0
    assert hasattr(mock_game, 'card_deck')
    
    # Verify the mocks were called
    mock_get_game.assert_called_once_with("test-game-id")
    mock_save_game.assert_called_once_with(mock_game)

@pytest.mark.asyncio
@patch('services.game_service.get_game_from_redis')
@patch('services.game_service.start_game')
async def test_reset_game_nonexistent(mock_start_game, mock_get_game):
    # Setup mock for non-existent game
    mock_get_game.return_value = None
    mock_start_game.return_value = {"message": "Game started", "game_id": "new-game-id", "user_id": "test-user"}
    
    # Call the function
    result = await reset_game("nonexistent-id", "test-user")
    
    # Verify start_game was called
    mock_get_game.assert_called_once_with("nonexistent-id")
    mock_start_game.assert_called_once_with("test-user")
    
    # Verify the result
    assert result == {"message": "Game started", "game_id": "new-game-id", "user_id": "test-user"}

# Test the pull_card function
@pytest.mark.asyncio
@patch('services.game_service.get_game_from_redis')
@patch('services.game_service.save_game_to_redis')
async def test_pull_card_success(mock_save_game, mock_get_game):
    # Setup mock for existing game
    mock_game = MagicMock()
    mock_game.gameid = "test-game-id"
    mock_game.userid = "test-user"
    mock_game.currRnd = 1
    mock_game.card_deck = {
        'Hearts': ['A', '2', '3'],
        'Diamonds': ['K', 'Q', 'J']
    }
    mock_get_game.return_value = mock_game
    
    # Call the function
    result = await pull_card("test-user", "test-game-id")
    
    # Verify the result
    assert "message" in result
    assert "game_id" in result
    assert "user_id" in result
    assert "round" in result
    assert "cards" in result
    assert result["game_id"] == "test-game-id"
    assert result["user_id"] == "test-user"
    assert result["round"] == 1
    assert result["cards"]["Hearts"] == "2"
    assert result["cards"]["Diamonds"] == "Q"
    
    # Verify the game was updated
    assert mock_game.currRnd == 2
    
    # Verify the mocks were called
    mock_get_game.assert_called_once_with("test-game-id")
    mock_save_game.assert_called_once_with(mock_game)

@pytest.mark.asyncio
@patch('services.game_service.get_game_from_redis')
async def test_pull_card_game_not_found(mock_get_game):
    # Setup mock for non-existent game
    mock_get_game.return_value = None
    
    # Call the function
    result = await pull_card("test-user", "nonexistent-id")
    
    # Verify the result
    assert "error" in result
    assert "Game with ID nonexistent-id not found" in result["error"]
    
    # Verify the mock was called
    mock_get_game.assert_called_once_with("nonexistent-id")

@pytest.mark.asyncio
@patch('services.game_service.get_game_from_redis')
async def test_pull_card_wrong_user(mock_get_game):
    # Setup mock for game with different user
    mock_game = MagicMock()
    mock_game.gameid = "test-game-id"
    mock_game.userid = "other-user"
    mock_get_game.return_value = mock_game
    
    # Call the function
    result = await pull_card("test-user", "test-game-id")
    
    # Verify the result
    assert "error" in result
    assert "User ID does not match" in result["error"]
    
    # Verify the mock was called
    mock_get_game.assert_called_once_with("test-game-id")
