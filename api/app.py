from fastapi import Depends, FastAPI
from fastapi_simple_security import api_key_router, api_key_security
from public import tabquery_public
from private import tabquery_private
# from database import crud, models, schemas
# from database.database import SessionLocal, engine
# from sqlalchemy.orm import Session

# models.Base.metadata.create_all(bind=engine)

app = FastAPI(description="TableQuery. Say Goodbye to writing long and boring SQL Statements.",title="TableQuery")

# # Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()




app.include_router(api_key_router, prefix="/auth", tags=["_auth"])
app.include_router(tabquery_public.router)
app.include_router(tabquery_private.router)


@app.get("/secure", dependencies=[Depends(api_key_security)])
async def secure_endpoint():
    return {"message": "This is a secure endpoint"}


@app.get("/")
async def docs():
    return "Welcome to TableQuery API"

# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)



