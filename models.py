from pydantic import BaseModel, EmailStr
from typing import Optional, Any, Dict, Union, List

class Game(BaseModel):
    """
    Represents a game in the system.
    
    Attributes:
        gameid: Unique identifier for the game
        userid: ID of the user who owns this game
        currRnd: Current round number in the game
        card_deck: Dictionary containing the card deck organized by suits
    """
    gameid: str
    currRnd: int
    card_deck: Dict[str, List[str]]

class User(BaseModel):
    """
    Represents a user in the system.
    
    Attributes:
        userid: Unique identifier for the user
        username: User's username
        email: User's email address
        full_name: User's full name (optional)
        games: List of game IDs associated with this user
    """
    userid: str
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    games: List[str] = []

class APIResponse(BaseModel):
    status_code: int
    message: str
    game: Optional[Game] = None
    user: Optional[User] = None
    data: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True
