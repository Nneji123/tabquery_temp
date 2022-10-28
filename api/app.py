import os

from fastapi import Depends, FastAPI, HTTPException, status, File, UploadFile
from utils import execute_query_csv, execute_query_excel, execute_query_parquet
from fastapi.security import HTTPBearer
# from schemas import Question

app = FastAPI()
token_auth_scheme = HTTPBearer()

@app.get('/')
async def docs():
    return "Welcome to TableQuery API"


@app.post("/api/private/query-csv", tags=["table-query-csv"], summary="Post query and get answer")
async def get_table_csv(token: str = Depends(token_auth_scheme),question: str, file: UploadFile = File(...)):
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
    
    Doc Author:
        Ifeanyi
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
        

@app.post("/api/private/query-excel", tags=["table-query-excel"], summary="Post query and get answer")
async def get_table_csv(question:str, file: UploadFile = File(...)):
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
    
    Doc Author:
        Ifeanyi
    """
    if file.content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
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
        
@app.post("/api/public/query-csv", tags=["table-query-csv"], summary="Post query and get answer")
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
        

@app.post("/api/public/query-excel", tags=["table-query-excel"], summary="Post query and get answer")
async def get_table_csv(question:str, file: UploadFile = File(...)):
    if file.content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
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
        
