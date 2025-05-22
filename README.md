# Getting Started app for Discord

This project contains a port of the
Sweaters and Hedgehog TTRPG Game over at itch.to,
FastAPI/Python/Redis API backend

Overview of API calls via http://0.0.0.0:8000/docs

## Project structure
Below is a basic overview of the project structure:

```
├── assets   -> any images
├── exceptions --> for custom exceptions
├── locales --> internationalization (may be incomplete)
├── logs --> log dir
├── services
├── ├── game_service.py --> runs game code
├── ├── redis_service.oy --> all the CRUD DB code
├── ├── user_service.py --> all the user code (adding, deleting, listing)
├── tests --> unit tests
├── utils
├── ├── logger.py --> logging config
├── Dockerfile --> docker config
├── pytest.ini --> pytest config
├── .env -> .env file
├── main.py    -> main entrypoint for app
├── models.py -> all data models
├── run.sh --> docker run file
├── requirements.txt --> python required libs
├── README.md
└── .gitignore
```
