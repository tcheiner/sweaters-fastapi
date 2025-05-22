import random
from fastapi.exceptions import HTTPException
from uuid import uuid4
from models import Game
from services.redis_service import save_game_to_redis, get_game_from_redis
from services.user_service import add_game_to_user
from utils.logger import logger


class DeckCards:
    def __init__(self, suits=None):
        self.suits = suits or ['Hearts', 'Diamonds', 'Clubs', 'Spades']

    def shuffle(self, array):
        for i in range(len(array) - 1, 0, -1):
            j = random.randint(0, i)
            array[i], array[j] = array[j], array[i]
        return array

    def initialize_deck(self):
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        deck = {}
        for suit in self.suits:
            shuffled = self.shuffle(values[:])
            deck[suit] = shuffled
        return deck

# Function to start a new game
async def start_game(userid: str = None):
    # If userid is None, set it to "guest"
    if userid is None:
        userid = "guest"
        
    # Create a new deck and initialize it
    deck = DeckCards()
    card_deck = deck.initialize_deck()

    # Create a new game
    new_game = Game(
        gameid=str(uuid4()),
        userid=userid,
        currRnd=1,
        card_deck=card_deck
    )
    
    # Associate the game with the user (now always has a value)
    try:
        # Save the game to Redis
        await save_game_to_redis(new_game)
        await add_game_to_user(userid, new_game.gameid)
    except Exception as e:
        # Log the error but continue - the game was created successfully
        logger.error(f"Failed to add game {new_game.gameid} to user {userid}: {str(e)}")

    return {"message": "Game started", "game_id": new_game.gameid, "user_id": userid}

# Function to reset a game
async def reset_game(gameid: str = None, userid: str = None):
    # If userid is None, set it to "guest"
    if userid is None:
        userid = "guest"
        
    if not gameid:
        # If no game ID is provided, just start a new game
        return await start_game(userid)
    
    # Get the existing game
    game = await get_game_from_redis(gameid)
    
    if not game:
        # If game doesn't exist, start a new one
        return await start_game(userid)
        
    # Check if the user ID matches
    if game.userid != userid:
        return {"error": "User ID does not match the game owner", "game_id": game.gameid, "user_id": userid}
    
    # Reset the game by shuffling the deck and setting currRnd to 0
    deck = DeckCards()
    game.card_deck = deck.initialize_deck()
    game.currRnd = 0
    
    # Save the updated game to Redis
    await save_game_to_redis(game)
    
    return {"message": "Game reset", "game_id": game.gameid, "user_id": userid}

# Function to pull a card from the game
async def pull_card(userid: str, gameid: str, endpoint: str = None, function: str = None):
    # Validate input parameters
    if not userid:
        raise HTTPException("User ID is required")
    if not gameid:
        raise HTTPException("Game ID is required")
    
    # Get the existing game
    from services.redis_service import get_game_from_redis, save_game_to_redis
    game = await get_game_from_redis(gameid, endpoint, function)
    
    if not game:
        raise HTTPException(f"Game with ID {gameid} not found")
    
    # Check if the user ID matches
    if game.userid != userid and userid != "guest":
        raise HTTPException(f"User ID {userid} does not match the game owner {game.userid}")
    
    # Get the current round
    current_round = game.currRnd
    
    # Prepare the response with cards from the current round
    pulled_cards = {}
    for suit, cards in game.card_deck.items():
        if current_round < len(cards):
            pulled_cards[suit] = cards[current_round]
    
    # Increment the round counter
    game.currRnd += 1
    
    # Save the updated game back to Redis
    await save_game_to_redis(game)
    
    return {
        "message": "Card pulled successfully",
        "game_id": game.gameid,
        "user_id": game.userid,
        "round": current_round,
        "cards": pulled_cards
    }
