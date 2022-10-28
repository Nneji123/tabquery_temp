import sys

sys.path.append("..")

from fastapi import (
    APIRouter,
    Depends,
    FastAPI,
    File,
    HTTPException,
    Response,
    UploadFile,
    status,
)

router = APIRouter()

from inference import *


@router.post(
    "/api/v1/public/query-csv",
    tags=["public"],
    summary="Post query and get answer",
)
async def get_table_csv(question: str, file: UploadFile = File(...)):
    if file.content_type != "application/vnd.ms-excel":
        raise HTTPException(400, detail="Invalid document type")
        return {"filename": "file.filename"}
    else:
        files = await file.read()
        # save the file
        filename = "data/filename.csv"
        with open(filename, "wb+") as f:
            f.write(files)
        # open the file and return the file name
        try:
            data = execute_query_csv(question, "data/filename.csv")
            if os.path.exists("data/filename.csv"):
                os.remove("data/filename.csv")
            return data
        except ValueError as e:
            return {"error": str(e)}


@router.post(
    "/api/v1/public/query-excel",
    tags=["public"],
    summary="Post query and get answer",
)
async def get_table_csv(question: str, file: UploadFile = File(...)):
    if (
        file.content_type
        != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ):
        raise HTTPException(400, detail="Invalid document type")
        return {"filename": "file.filename"}
    else:
        files = await file.read()
        # save the file
        filename = "data/filename.xlsx"
        with open(filename, "wb+") as f:
            f.write(files)
        # open the file and return the file name
        try:
            data = execute_query_excel(question, "data/filename.xlsx")
            if os.path.exists("data/filename.xlsx"):
                os.remove("data/filename.xlsx")
            return data
        except ValueError as e:
            return {"error": str(e)}


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
