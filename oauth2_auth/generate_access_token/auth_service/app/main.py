from fastapi import FastAPI
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from typing import Annotated
from fastapi import HTTPException

app = FastAPI()


@app.get("/")
def read_root():
    return "Hello World"


# generate acess token
ALGORITHM = "HS256"
SECRET_KEY = "A Secure Secret Key"


def create_access_token(subject: str , expires_delta: timedelta) -> str:
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



@app.get('/get_access_token')
def access_token(username):
    access_token_expires = timedelta(minutes=1)
    token = create_access_token(subject=username, expires_delta=access_token_expires)
    return token   
         


def decode_access_token(access_token: str):
    decoded_jwt = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    return decoded_jwt         
         

@app.get('/decode_access_token')
def decode_token(access_token):
    try:
        decoded_token_data = decode_access_token(access_token)
        return {"decoded_token": decoded_token_data}
    except JWTError as e:
        return {"error": str(e)}
    

# implement_auth    

fake_users_db: dict[str, dict[str, str]] = {
    "ameenalam": {
        "username": "ameenalam",
        "full_name": "Ameen Alam",
        "email": "ameenalam@example.com",
        "password": "ameenalamsecret",
    },
    "mjunaid": {
        "username": "mjunaid",
        "full_name": "Muhammad Junaid",
        "email": "mjunaid@example.com",
        "password": "mjunaidsecret",
    },
}

@app.post('/login')
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)]):
    user_in_fakedb = fake_users_db.get(form_data.username)
    # print("User in fake db",user_in_fakedb)
    # User in fake db {'username': 'ameenalam', 'full_name': 'Ameen Alam', 'email': 'ameenalam@example.com', 'password': 'ameenalamsecret'}
    if not user_in_fakedb:
        raise HTTPException(status_code=400, detail="Incorrect username")
    
    if not form_data.password == user_in_fakedb["password"]:
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    access_token_expires = timedelta(minutes=1)
    token = create_access_token(subject=user_in_fakedb["username"], expires_delta=access_token_expires) 


    return {"access_token": token, "token_type": "bearer", "expires_in": access_token_expires.total_seconds() }



    
    