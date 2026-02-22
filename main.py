from fastapi import FastAPI, UploadFile, File, Header, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import csv
import io

app = FastAPI()

# 🔥 GLOBAL CORS (REQUIRED FOR GRADER)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)

UPLOAD_TOKEN = "ocj4rq3opn4c934t"
MAX_SIZE = 64 * 1024  # 64KB

@app.options("/upload")
async def options_handler():
    return Response(status_code=200)

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    x_upload_token_5889: str = Header(None)
):

    # 🔐 Authentication
    if x_upload_token_5889 != UPLOAD_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # 📁 File type validation
    if not file.filename.endswith((".csv", ".json", ".txt")):
        raise HTTPException(status_code=400, detail="Invalid file type")

    content = await file.read()

    # 📏 File size validation
    if len(content) > MAX_SIZE:
        raise HTTPException(status_code=413, detail="File too large")

    # 📊 Process CSV
    text_stream = io.StringIO(content.decode("utf-8"))
    reader = csv.DictReader(text_stream)

    rows = list(reader)
    columns = reader.fieldnames

    total_value = sum(float(row["value"]) for row in rows)

    category_counts = {}
    for row in rows:
        cat = row["category"]
        category_counts[cat] = category_counts.get(cat, 0) + 1

    return {
        "email": "23f2003236@ds.study.iitm.ac.in",
        "filename": file.filename,
        "rows": len(rows),
        "columns": columns,
        "totalValue": round(total_value, 2),
        "categoryCounts": category_counts
    }