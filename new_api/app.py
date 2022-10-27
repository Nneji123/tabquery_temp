import os

from fastapi import Depends, FastAPI, HTTPException, status, File, UploadFile
from utils import execute_query_csv, execute_query_excel, execute_query_parquet
from schemas import Question

app = FastAPI()

@app.get('/')
async def docs():
    return "Welcome to TableQuery API"


@app.post("/query_csv", tags=["table-query-csv"], summary="Post query and get answer")
async def get_table_csv(query: Question, file: UploadFile = File(...)):
    if file.content_type != "application/vnd.ms-excel":
        raise HTTPException(400, detail="Invalid document type")
        return {"filename": "file.filename"}
    else:
        files = await file.read()
        # save the file
        filename = "filename.csv"
        with open(filename, "wb+") as f:
            f.write(files)
        # open the file and return the file name
        try:
            data = execute_query_csv(str(query.quest), "filename.csv")
            if os.path.exists("filename.csv"):
                os.remove("filename.csv")
            return data
        except ValueError as e:
            return {"error": str(e)}
        

@app.post("/query_excel", tags=["table-query-excel"], summary="Post query and get answer")
async def get_table_csv(question:str, file: UploadFile = File(...)):
    if file.content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        raise HTTPException(400, detail="Invalid document type")
        return {"filename": "file.filename"}
    else:
        files = await file.read()
        # save the file
        filename = "filename.xlsx"
        with open(filename, "wb+") as f:
            f.write(files)
        # open the file and return the file name
        try:
            data = execute_query_excel(question, "filename.xlsx")
            if os.path.exists("filename.xlsx"):
                os.remove("filename.xlsx")
            return data
        except ValueError as e:
            return {"error": str(e)}
        
@app.post("/query_parquet", tags=["table-query-parquet"], summary="Post query and get answer")
async def get_table_csv(question:str, file: UploadFile = File(...)):
    if file.content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        raise HTTPException(400, detail="Invalid document type")
        return {"filename": "file.filename"}
    else:
        files = await file.read()
        # save the file
        filename = "filename.parquet"
        with open(filename, "wb+") as f:
            f.write(files)
        # open the file and return the file name
        try:
            data = execute_query_parquet(question, "filename.parquet")
            if os.path.exists("filename.parquet"):
                os.remove("filename.parquet")
            return data
        except ValueError as e:
            return {"error": str(e)}
        