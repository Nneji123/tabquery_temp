from fastapi import Depends, FastAPI
from fastapi_auth import api_key_router, api_key_security
from private import tabquery_private
from public import tabquery_public

app = FastAPI(
    description="Say Goodbye to writing long and boring SQL Statements.",
    title="TableQuery",
    version=1.0,
)


app.include_router(api_key_router, prefix="/auth", tags=["_auth"])
app.include_router(tabquery_public.router, prefix="/api/v1/public", tags=["public"])
app.include_router(tabquery_private.router, prefix="/api/v1/private", tags=["private"])


@app.get("/secure", dependencies=[Depends(api_key_security)])
async def secure_endpoint():
    return {"message": "This is a secure endpoint"}


@app.get("/")
async def docs():
    return "Welcome to TableQuery API"
