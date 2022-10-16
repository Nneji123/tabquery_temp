import os

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from utils import execute_query

app = FastAPI(
    title="Table Query API",
    description="""An API for querying tables with natural language."""
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=PlainTextResponse, tags=["home"])
async def home():
    note = """
    Table Query API 📚
    An API for querying tables with natural language.
    Note: add "/redoc" to get the complete documentation.
    """
    return note


@app.post("/table-quey", tags=["table-query"])
async def get_table(question:str, file: UploadFile = File(...)):
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
    
