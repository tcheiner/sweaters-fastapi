import logging
import json
import os
from datetime import datetime

# Configure logging
def setup_logger():
    logger = logging.getLogger("sweaters-api")
    logger.setLevel(logging.INFO)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Create file handler
    file_handler = logging.FileHandler(f"logs/api_{datetime.now().strftime('%Y%m%d')}.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    
    # Add file handler to logger
    logger.addHandler(file_handler)
    
    return logger

# Create a function to log API calls
def log_api_call(endpoint, method, request_data=None, response_data=None, user=None, game=None, message=None):
    logger = logging.getLogger("sweaters-api")
    
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "endpoint": endpoint,
        "method": method,
        "request_data": request_data,
    }
    
    if response_data:
        # Extract only necessary fields to avoid circular references
        log_data["response"] = {
            "status_code": response_data.status_code,
            "message": response_data.message
        }
    
    if user:
        log_data["user"] = {
            "userid": user.userid,
            "username": user.username,
            "games_count": len(user.games) if hasattr(user, "games") else 0
        }
    
    if game:
        log_data["game"] = {
            "gameid": game.gameid,
            "userid": game.userid,
            "currRnd": game.currRnd
        }

    if message:
        log_data["message"] = message
    
    logger.info(f"API Call: {json.dumps(log_data, default=str)}")
    return log_data


def log_func_call(error_msg=None):
    logger = logging.getLogger("sweaters-api")

    log_data = {
        "timestamp": datetime.now().isoformat(),
        "message": error_msg
    }

    return log_data

logger = setup_logger()
