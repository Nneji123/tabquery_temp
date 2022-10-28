from fastapi import Depends, FastAPI
from fastapi_simple_security import api_key_router, api_key_security
from public import tabquery_public

app = FastAPI()

app.include_router(api_key_router, prefix="/auth", tags=["_auth"])
app.include_router(tabquery_public.router)


@app.get("/secure", dependencies=[Depends(api_key_security)])
async def secure_endpoint():
    return {"message": "This is a secure endpoint"}


@app.get("/")
async def docs():
    return "Welcome to TableQuery API"


# @app.post("/query_parquet", tags=["table-query-parquet"], summary="Post query and get answer")
# async def get_table_csv(question:str, file: UploadFile = File(...)):
#     if file.content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
#         raise HTTPException(400, detail="Invalid document type")
#         return {"filename": "file.filename"}
#     else:
#         files = await file.read()
#         # save the file
#         filename = "filename.parquet"
#         with open(filename, "wb+") as f:
#             f.write(files)
#         # open the file and return the file name
#         try:
#             data = execute_query_parquet(question, "filename.parquet")
#             if os.path.exists("filename.parquet"):
#                 os.remove("filename.parquet")
#             return data
#         except ValueError as e:
#             return {"error": str(e)}
