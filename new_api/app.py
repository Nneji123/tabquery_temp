import os

from fastapi import Depends, FastAPI, HTTPException, status, File, UploadFile
from replit import db
from utils import execute_query

app = FastAPI()

@app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')


@app.post("/query_csv", tags=["table-query"], summary="Post query and get answer", response_model=UserOut)
async def get_table(question:str, file: UploadFile = File(...)):
    if file.content_type != "application/java-archive":
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
            data = execute_query(question, "filename.csv")
            if os.path.exists("filename.csv"):
                os.remove("filename.csv")
            return data
        except ValueError as e:
            return {"error": str(e)}
        