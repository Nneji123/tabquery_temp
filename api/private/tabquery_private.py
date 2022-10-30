import sys

sys.path.append("..")

from fastapi import APIRouter

router = APIRouter()

from fastapi import (APIRouter, Depends, FastAPI, File, HTTPException,
                     Response, UploadFile, status)
from fastapi_simple_security import api_key_router, api_key_security
from inference import *

# app = FastAPI()

router.include_router(api_key_router, prefix="/auth", tags=["_auth"])


@router.post(
    "/api/v1/private/query-csv",
    tags=["private"],
    summary="Post query and get answer",
    dependencies=[Depends(api_key_security)],
)
async def get_table_csv(question: str, file: UploadFile = File(...)):
    """
    The get_table_csv function is used to get a table from a csv file.
    It takes in the question and the file as parameters. It then reads the file, saves it, and executes
    the query on it.

    Args:
        token:str=Depends(token_auth_scheme): Ensure that the user has provided a valid token
        question:str: Pass the sql query to the function
        file:UploadFile=File(...): Upload a file

    Returns:
        A dictionary that contains the file name and the data
    """

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
    "/api/v1/private/query-excel",
    tags=["private"],
    summary="Post query and get answer",
    dependencies=[Depends(api_key_security)],
)
async def get_table_csv(question: str, file: UploadFile = File(...)):
    """
    The get_table_csv function accepts a question and an excel file as parameters.
    It then saves the excel file to the server, executes a query using the question and
    the saved excel file, returns that data in csv format, and finally deletes all files from
    the server.

    Args:
        question:str: Pass the question that is being asked to the user
        file:UploadFile=File(...): Get the file from the client

    Returns:
        The data in the excel file
    """
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
