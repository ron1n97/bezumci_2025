import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import qrcode

app = FastAPI()
# Разрешаем запросы со всех источников (можно сузить)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Можно указать ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST и т. д.)
    allow_headers=["*"],  # Разрешить все заголовки
)
SHARED_DIR = Path(__file__).parent.parent / "shared_qr"
app.mount("/shared", StaticFiles(directory=SHARED_DIR), name="static")


# Эндпоинт для загрузки запроса
@app.post("/upload-request")
async def upload_request(file: UploadFile = File(...)):
    file_path = SHARED_DIR / "requests" / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"status": "ok"}


# Эндпоинт для проверки ответа
@app.get("/get-response/{request_id}")
async def get_response(request_id: str):
    response_path = SHARED_DIR / "responses" / f"response_{request_id}.png"
    if not response_path.exists():
        raise HTTPException(status_code=404)
    return FileResponse(response_path)
