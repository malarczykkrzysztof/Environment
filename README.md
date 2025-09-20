# Python Environment for RestAPI

## Description
This is a development environment prepared with Docker Compose, based on Python.  
It installs the necessary libraries and suggests recommended extensions for VS Code.  
A simple FastAPI project with tests has also been implemented here.

## Technologies
- FastAPI
- Pydantic
- Uvicorn
- Redis
- Pytest
- pytest-cov
- pytest-watch
- HTTPX
- Ruff
- Requests
- PyMongo

## Installation
1. Start the project on your host machine: docker compose up
2. Install all recommended extensions in VS Code.
3. Click the blue icon in the bottom-left corner of VS Code and choose Attach to Running Container.
4. Select the container named /python-server.
5. Install any additional necessary extensions inside the container.
6. You are now ready to work inside the container.
7. To stop the project on your host machine: docker compose down


## Testing
On caontainer in code/app

- python -m pytest -vv
- python -m pytest --cov=app -vv
