from fastapi import Depends, FastAPI
from fastapi_simple_security import api_key_router, api_key_security
from public import tabquery_public
from private import tabquery_private

app = FastAPI()

app.include_router(api_key_router, prefix="/auth", tags=["_auth"])
app.include_router(tabquery_public.router)
app.include_router(tabquery_private.router)


@app.get("/secure", dependencies=[Depends(api_key_security)])
async def secure_endpoint():
    return {"message": "This is a secure endpoint"}


@app.get("/")
async def docs():
    return "Welcome to TableQuery API"


