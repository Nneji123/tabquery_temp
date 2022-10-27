import os

from fastapi import Depends, FastAPI, HTTPException, status, File, UploadFile
from utils import execute_query_csv, execute_query_excel, execute_query_parquet

app = FastAPI()

@app.get('/')
async def docs():
    return "Welcome to TableQuery API"


@app.post("/query_csv", tags=["table-query"], summary="Post query and get answer")
async def get_table_csv(question:str, file: UploadFile = File(...)):
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
            data = execute_query_csv(question, "filename.csv")
            if os.path.exists("filename.csv"):
                os.remove("filename.csv")
            return data
        except ValueError as e:
            return {"error": str(e)}
        