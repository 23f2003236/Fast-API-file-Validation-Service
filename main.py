from fastapi import FastAPI, UploadFile, File, Header, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import csv
import io
import os

app = FastAPI()

# ✅ Enable CORS for POST from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

MAX_SIZE = 64 * 1024  # 64KB
VALID_EXTENSIONS = {".csv", ".json", ".txt"}
EXPECTED_TOKEN = "ocj4rq3opn4c934t"


@app.post("/upload")
async def validate_file(
    file: UploadFile = File(...),
    x_upload_token_5889: str = Header(None)
):

    # 🔐 1️⃣ Authentication check
    if x_upload_token_5889 != EXPECTED_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # 📄 2️⃣ File type check
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()

    if ext not in VALID_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # 📦 3️⃣ File size check
    contents = await file.read()

    if len(contents) > MAX_SIZE:
        raise HTTPException(status_code=413, detail="File too large")

    # 📊 4️⃣ If CSV, parse and analyze
    if ext == ".csv":

        decoded = contents.decode("utf-8")
        reader = csv.DictReader(io.StringIO(decoded))

        rows = list(reader)

        if not rows:
            raise HTTPException(status_code=400, detail="Empty CSV")

        columns = reader.fieldnames

        total_value = 0
        category_counts = {}

        for row in rows:
            if "value" in row:
                try:
                    total_value += float(row["value"])
                except:
                    pass

            if "category" in row:
                cat = row["category"]
                category_counts[cat] = category_counts.get(cat, 0) + 1

        return {
            "email": "23f2003236@ds.study.iitm.ac.in",
            "filename": filename,
            "rows": len(rows),
            "columns": columns,
            "totalValue": round(total_value, 2),
            "categoryCounts": category_counts
        }

    # For non-CSV valid files
    return {
        "email": "23f2003236@ds.study.iitm.ac.in",
        "filename": filename,
        "message": "Valid file"
    }