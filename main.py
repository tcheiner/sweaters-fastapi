from fastapi import FastAPI, HTTPException
from pydantic import EmailStr
from exceptions.exceptions import register_exception_handlers, UserNotFoundException
from services.game_service import start_game, reset_game, pull_card
from services.user_service import create_user, get_user, add_game_to_user
from services.redis_service import get_all_users_from_redis, get_game_from_redis
from models import APIResponse
from utils import logger

app = FastAPI()

register_exception_handlers(app)

# Routes

# Endpoint to create a new user
@app.post("/users/", response_model=APIResponse)
async def create_user_endpoint(username: str, email: EmailStr, full_name: str):
    usr = None
    msg = None
    status = None
    res = None
    try:
        # Attempt to create the user
        usr = await create_user(username, email, full_name)
        
        # Create successful response
        res = APIResponse(
            status_code=200,
            message="User created successfully",
            user=usr
        )
    except HTTPException as e:
        message= msg + e.detail
        res = APIResponse(
            status_code=500,
            message=f"{msg} {e.detail}",
            user=usr
        )
    finally:
        # Log the API call
        logger.log_api_call(
            endpoint="/users",
            method="create_user",
            request_data=f"username: {username}, email: {email}, full_name: {full_name}",
            response_data=res,
            user=usr,
            game=None,
            message=msg
        )
        return res


# Endpoint to fetch a user by ID
@app.get("/users/{userid}", response_model=APIResponse)
async def get_user_endpoint(userid: str):
    usr = None
    msg = None
    status = None
    res = None
    try:
        usr = await get_user(userid)
        res = APIResponse(
                status_code=200,
                message="User retrieved successfully",
                user=usr
            )
    except HTTPException as e:
        message = msg + e.detail
        response = APIResponse(
            status_code=500,
            message=f"{msg} {e.detail}",
            user=usr
        )
    finally:
        # Log the API call
        logger.log_api_call(
            endpoint=f"/users/{userid}",
            method="get_user",
            request_data=f"userid: {userid}",
            response_data=res,
            user=usr,
            game=None,
            message=msg
        )
        return res

# Endpoint to add a game to a user
@app.post("/users/{userid}/games/", response_model=APIResponse)
async def add_game_to_user_endpoint(userid: str, gameid: str):
    usr = None
    msg = None
    status = None
    res = None
    try:
        user = await add_game_to_user(userid, gameid, endpoint="/users/{userid}/games/", function="add_game_to_user_endpoint")
        res =  APIResponse(
                status_code=200,
                message="Game added to user successfully",
                user=user
            )
    except HTTPException as e:
        msg =f"{msg} {e.detail}"
        res = APIResponse(
                status_code=500,
                message=f"{msg} {e.detail}",
                user=usr
            )
    finally:
        # Log the API call
        logger.log_api_call(
            endpoint=f"/users/{userid}/games/",
            method="add game to user",
            request_data=f"userid: {userid}",
            response_data=res,
            user=usr,
            game=None,
            message=msg
        )
        return res

@app.get("/start-game", response_model=APIResponse)
async def start_game_endpoint(userid: str = None):
    """
    Start a new game and optionally associate it with a user.
    
    Parameters:
    - userid: Optional user ID to associate the game with (defaults to "guest" if None)
    """
    usr = None
    msg = None
    status = None
    res = None
    try:
        result = await start_game(userid)

        # Check if there was an error
        if "error" in result:
            res =  APIResponse(
                    status_code=400,
                    message=result["error"],
                    data=result
                )

            res =  APIResponse(
                    status_code=200,
                    message=result["message"],
                    data=result
                )
    except HTTPException as e:
        msg = f"{msg} {e.detail}"
        res = APIResponse(
            status_code=500,
            message=f"{msg} {e.detail}",
            user=usr
        )
    finally:
        # Log the API call
        logger.log_api_call(
            endpoint=f"/start-game",
            method="start-game",
            request_data=f"userid: {userid}",
            response_data=res,
            user=usr,
            game=None,
            message=msg
        )
        return res


@app.post("/reset-game", response_model=APIResponse)
async def reset_game_endpoint(gameid: str = None, userid: str = None):
    """
    Reset an existing game or create a new one if game ID is not provided.
    
    Parameters:
    - gameid: Optional game ID to reset
    - userid: Optional user ID to associate with the game (defaults to "guest" if None)
    """
    usr = None
    msg = None
    status = None
    res = None
    result = await reset_game(gameid, userid)
    
    # Check if there was an error
    if "error" in result:
        return APIResponse(
            status_code=400,
            message=result["error"],
            data=result
        )
    
    return APIResponse(
        status_code=200,
        message=result["message"],
        data=result
    )

@app.get("/users", response_model=APIResponse)
async def list_users_endpoint():
    """
    List all users in the database.
    
    Returns:
    - A list of all users
    """
    usr = None
    msg = None
    status = None
    res = None
    users = await get_all_users_from_redis()
    return APIResponse(
        status_code=200,
        message="Users retrieved successfully",
        data={"users": users}
    )

@app.get("/pull-card", response_model=APIResponse)
async def pull_card_endpoint(userid: str, gameid: str):
    """
    Pull a card from the game for the specified user.
    
    Parameters:
    - userid: User ID (required)
    - gameid: Game ID (required)
    
    Returns:
    - The pulled card information or an error message
    """
    usr = None
    msg = None
    status = None
    res = None
    try:
        result = await pull_card(userid, gameid, endpoint="/pull-card", function="pull_card_endpoint")
        
        # Get the game after the card was pulled
        game = await get_game_from_redis(gameid)
        
        # Get the user
        from services.user_service import get_user
        user = await get_user(userid) if userid != "guest" else None
        
        return APIResponse(
            status_code=200,
            message=result["message"],
            game=game,
            user=user,
            data=result
        )
    except Exception as e:
        # Handle any exceptions that occur during the pull_card operation
        return APIResponse(
            status_code=400,
            message=str(e),
            data={"error": str(e)}
        )
