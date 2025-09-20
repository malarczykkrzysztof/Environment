from fastapi.testclient import TestClient
import pytest

from unittest.mock import patch, Mock

from app.main import app
from app.models.user import User 
from app.models.user import UserSafe

test_user1 = User( first_name= "Jan", last_name= "Kowalski", email= "Kowalski@Email.com", password= "mypassword")
test_user2 = User( first_name= "Piotr", last_name= "Malik", email= "Malik@Email.com", password= "malik")

client = TestClient(app)

@pytest.fixture
def mocked_database_fix2():
    with patch("app.main.Database") as mocked_database:
        database_instance = Mock()
        database_instance.get_all_users.return_value = [test_user1, test_user2]
        database_instance.get_one_user.return_value = test_user1
        database_instance.user_update.return_value = {"Info ": f"User with email Kowalski@Email.com modified in db"}
        database_instance.delete_user.return_value = {"Info ": f"User with email Kowalski@Email.com removed in db"}
        database_instance.add_user.return_value = {"Info ": f"User with email Kowalski@Email.com added in db"}
        database_instance.delete_users.return_value = {"Info ": f"Deleted 1 users from DB"}
        database_instance.add_users.return_value = [test_user1, test_user2]
        
        
        
        mocked_database.return_value = database_instance
        yield mocked_database

def test_users_all3(mocked_database_fix2):
    response = client.get("/user")
    assert response.status_code == 200
    expected_result = [
        {
        "first_name": "Jan", 
        "last_name": "Kowalski",
        "email": "Kowalski@Email.com"
        },
        {"first_name": "Piotr",
         "last_name": "Malik",
         "email": "Malik@Email.com"
        }
    ]
    assert response.json() == expected_result   
    
    
def test_user_one(mocked_database_fix2):
    response = client.get("/users/Kowalski@Email.com")
    assert response.status_code == 200
    expected_result = {
        "first_name": "Jan", 
        "last_name": "Kowalski",
        "email": "Kowalski@Email.com"
        } 
    assert response.json() == expected_result   
    
def test_user_update(mocked_database_fix2):
    response = client.put("/users",json = test_user1.model_dump())
    assert response.status_code == 200
    assert response.json() == {"Info ": f"User with email Kowalski@Email.com modified in db"} 
    
def test_delete_user_by_email(mocked_database_fix2):
    response = client.delete("/users/test@email.com")
    assert response.status_code == 200
    assert response.json() == {"Info ": f"User with email Kowalski@Email.com removed in db"}
    
def test_add_user(mocked_database_fix2):
    response = client.post("/users",json = test_user1.model_dump())
    assert response.status_code == 201
    assert response.json() == {"Info ": f"User with email Kowalski@Email.com added in db"}
    
def test_delete_users(mocked_database_fix2):
    response = client.delete("/users/")
    assert response.status_code == 200     
    assert response.json() == {"Info ": f"Deleted 1 users from DB"}

def test_add_users(mocked_database_fix2):
    response = client.post("/users/")
    assert response.status_code == 201
    expected_result = [
        {
        "first_name": "Jan", 
        "last_name": "Kowalski",
        "email": "Kowalski@Email.com"
        },
        {"first_name": "Piotr",
         "last_name": "Malik",
         "email": "Malik@Email.com"
        }
    ]
    assert response.json() == expected_result 
