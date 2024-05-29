from fastapi import FastAPI
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from typing import Annotated
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
app = FastAPI()


@app.get("/")
def read_root():
    return "Hello World"


# generate acess token

#Access Tokens
#Access tokens are like digital keys that allow applications to access resources on behalf of a user.

#A "token" is just a string with some content that we can use later to verify this user. Normally, a token is set to expire after some time.

#Imagine you have a library card (access token) that lets you borrow books (access resources) from a library (API). The library card has your information and permissions about what books you can borrow. Similarly, an access token contains information about the user and what they are allowed to access.


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
        #{ "decoded_token": {"exp": 1716962552,"sub": "ameenalam"}} 
    except JWTError as e:
        return {"error": str(e)}
    

# implement_auth    

#Authentication
#The password "flow" is one of the ways ("flows") defined in OAuth2, to handle security and authentication.

#Here we will learn how to build Login System that can take username/email and returns Bearer token - yes access_token.

#We will be using the code from last step as starter code.


# FormData - What is it?
# FormData and JSON are both used to send data to an API. Just like we learned to pass data in JSON format in Body to APIs. FormData is a way to send data to an API.

# Format: FormData is a set of key/value pairs that can be sent using the multipart/form-data encoding type.
# Usage: When you submit a form in a web page, the browser automatically encodes the form data as FormData and sends it to the server.



# OAuth2PasswordRequestForm - A BuiltIn FastAPI Class Dependency
# OAuth2PasswordRequestForm is a class dependency that declares a form body with:

# The username.
# The password.
# Some Optional Fields...
# We can import it from fastapi.security import OAuth2PasswordRequestForm

# It is just a class dependency that you could have written yourself, or you could have declared Form parameters directly. But as it's a common use case, it is provided by FastAPI directly.

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



# @app.get('/all-users')
# def get_all_users():
#     return fake_users_db
#If we don't have authorizes user then everyone can acess this route.

# @app.get('/user/me')
# def get_user_me(acess_token):
#     acess_token = decode_access_token(acess_token)


#     users_in_db = fake_users_db.get(acess_token["sub"])

#     return users_in_db

    


#authorize_endpoints


# Authorization -
# So far we have learned to build an authentication flow in FastAPI following OAuth2 password flow specification.

# Now it's time to learn about authorization. So only an authorized user can access our APIs.

# We will be using the code from last step as starter code. Let's start by learning about the special security class provided by FastAPI to handle this.

# OAuth2PasswordBearer - A Special FastAPI Security Class
# OAuth2PasswordBearer is a special FastAPI Security Class that will let us authorize our APIs and the OpenAPI Docs(locahost:8000/docs) generated by it as well.

# We can import it from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
#This is callable so that we can use it in DependencyInjection



@app.get('/all-users')
def get_all_users(token: Annotated[str, Depends(oauth2_scheme)]):
    return fake_users_db

#Now,only authorize user can access this route

# Remember in last step we created a users/me endpoint and it was taking endpoint as query parameter. Now let's add proper authorization to it using the variable we have created in step 3. So our updated code is:

@app.get('/user/me')
def get_user_me(acess_token: Annotated[str, Depends(oauth2_scheme)]):
    acess_token = decode_access_token(acess_token)


    users_in_db = fake_users_db.get(acess_token["sub"])

    return users_in_db


# Now visit the Docs - there are 2 Notable differences

# 1. in the Endpoint /users/me:
#     - Calling this endpoint returns 401 unauthorized and 
#     - I don't have any option to pass token. 
# 2. There is a shiny `Authorize` Button and the top left corner. 
#     - Clicking on it we see the option to add username and email
# Try Authorize Button.
# Try Authorize button and pass dummy the username and password we declared in last step

# i.e: 
# "username": "ameenalam"
# "password": "ameenalamsecret"
# And viola it shows I am logged In - What's Next???

# -> Call the /users/me endpoint again and see what happens. On call now I get the user data