from fastapi import FastAPI, File, UploadFile
import os

SECRET = str(os.urandom(24).hex())
print(SECRET)
app = FastAPI()


# Now we can import and setup the LoginManager, which will handle the process of encoding and decoding our Json Web Tokens.

from fastapi_login import LoginManager

manager = LoginManager(SECRET, token_url="/auth/token")

# For the example we will use a dictionary to represent our user database. In your application this could also be a real database like sqlite or Postgres. It does not matter as you have to provide the function which retrieves the user.

fake_db = {"johndoe@e.mail": {"password": "hunter2"}}

# Now we have to provide the LoginManager with a way to load our user. The user_loader callback should either return your user object or None


@manager.user_loader()
async def load_user(email: str):  # could also be an asynchronous function
    user = fake_db.get(email)
    return user


# Now we have to define a way to let the user login in our app. Therefore we will create a new route:

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException

# the python-multipart package is required to use the OAuth2PasswordRequestForm
@app.post("/auth/token")
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user = load_user(email)  # we are using the same function to retrieve the user
    if not user:
        raise InvalidCredentialsException  # you can also use your own HTTPException
    elif password != user["password"]:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(data=dict(sub=email))
    return {"access_token": access_token, "token_type": "bearer"}


# Now whenever you want your user to be logged in to use a route, you can simply use your LoginManager instance as a dependency.


@app.get("/protected_tablequery")
async def get_table(question: str, file: UploadFile = File(...)):
    files = await file.read()
    # save the file
    filename = "filename.csv"
    with open(filename, "wb+") as f:
        f.write(files)
    # open the file and return the file name
    try:
        data = execute_query(question, "filename.csv")
        if os.path.exists("filename.csv"):
            os.remove("filename.csv")
        return data
    except ValueError as e:
        return {"error": str(e)}


# If you also want to handle a not authenticated error, you can add your own subclass of Exception to the LoginManager.

from starlette.responses import RedirectResponse


class NotAuthenticatedException(Exception):
    pass


# these two argument are mandatory
def exc_handler(request, exc):
    return RedirectResponse(url="/login")


# This will be deprecated in the future
# set your exception when initiating the instance
# manager = LoginManager(..., custom_exception=NotAuthenticatedException)
manager.not_authenticated_exception = NotAuthenticatedException
# You also have to add an exception handler to your app instance
# app.add_exception_handler(NotAuthenticatedException, exc_handler)

# To change the expiration date of the token use the expires_delta argument of the create_access_token method with a timedelta. The default is set 15 min. Please be aware that setting a long expiry date is not considered a good practice as it would allow an attacker with the token to use your application as long as he wants.

from datetime import timedelta

data = dict(sub=user.email)

# expires after 15 min
token = manager.create_access_token(data=data)
# expires after 12 hours
long_token = manager.create_access_token(data=data, expires=timedelta(hours=24))
