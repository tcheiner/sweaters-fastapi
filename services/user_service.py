from uuid import uuid4
from pydantic import EmailStr

from models import User
from services.redis_service import save_user_to_redis, get_user_from_redis


# Function to create a new user
async def create_user(username: str, email: EmailStr, full_name: str = None) -> User:
    # Generate a unique user ID
    userid = str(uuid4())

    # Create the user object
    new_user = User(
        userid=userid,
        username=username,
        email=email,
        full_name=full_name
    )

    # Save the user to Redis

    db_user = await save_user_to_redis(new_user)
    if db_user:
        return db_user
    else:
        return None

async def add_game_to_user(userid, gameid, endpoint: str = None, function: str = None) -> User:
    # If userid is "guest", create a temporary user object
    if userid == "guest":
        return User(
            userid="guest",
            username="Guest User",
            email="guest@example.com",
            games=[gameid]
        )
    
    # Find user
    user = await get_user_from_redis(userid, endpoint, function)
    # If user exists, add game to user
    if user:
        # Only add the game if it's not already in the list
        if gameid not in user.games:
            user.games.append(gameid)
            db_user = await save_user_to_redis(user)
            if db_user:
                return db_user
            else:
                return None
    # If user does not exist, return error
    else:
        return None
    return user

# Function to get a user by ID
async def get_user(userid: str) -> User:
    user = await get_user_from_redis(userid)
    if user:
        return user
    else:
        return None

