from fastapi import HTTPException

import redis
import os
from models import Game, User

# Get Redis URL from environment variables
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")  # Fallback to localhost if not set
redis_client = redis.from_url(REDIS_URL, decode_responses=True)


# Save a user to Redis
async def save_user_to_redis(user: User):
    key = f"user:{user.userid}"  # Use the user ID as the Redis key
    value = user.json()          # Convert the Pydantic model to JSON
    redis_client.set(key, value)
    return user

# Get a user from Redis
async def get_user_from_redis(userid: str, endpoint: str = None, function: str = None) -> User:
    key = f"user:{userid}"
    value = redis_client.get(key)  # Fetch the JSON string from Redis
    if value:
        return User.parse_raw(value)  # Convert the JSON string back to a Pydantic model
    return None  # Return None if the user doesn't exist

# Get all users from Redis
async def get_all_users_from_redis():
    # Get all keys that match the pattern "user:*"
    user_keys = redis_client.keys("user:*")
    users = []

    # Fetch each user's data
    for key in user_keys:
        value = redis_client.get(key)
        if value:
            users.append(User.parse_raw(value))

    return users

# Delete a user from Redis
async def delete_user_from_redis(userid: str, endpoint: str = None, function: str = None):
    key = f"user:{userid}"
    # Check if user exists before deleting
    if not redis_client.exists(key):
        raise HTTPException(status_code=404,
                            detail="delete_user_from_db: Cannot delete user with ID {userid} as it does not exist")
    return redis_client.delete(key)

# Save a game to Redis
async def save_game_to_redis(game: Game):
    key = f"game:{game.gameid}"  # Use the game ID as the Redis key
    value = game.json()  # Convert the Pydantic model to JSON
    redis_client.set(key, value)
    return game

# Get a game from Redis
async def get_game_from_redis(gameid: str, endpoint: str = None, function: str = None) -> Game:
    key = f"game:{gameid}"
    value = redis_client.get(key)
    if value:
        return Game.parse_raw(value)  # Convert the JSON string back to a Pydantic model
    return None

# Delete a game from Redis
async def delete_game_from_redis(gameid: str, endpoint: str = None, function: str = None):
    key = f"game:{gameid}"
    # Check if game exists before deleting
    if not redis_client.exists(key):
        raise HTTPException(status_code=404,
                            detail=f"delete game from db: Cannot delete game with ID {gameid} as it does not exist")
    return redis_client.delete(key)
