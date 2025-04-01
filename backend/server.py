import re
from fastapi import FastAPI, Request, HTTPException, APIRouter
from fastapi.responses import JSONResponse
import time
import os
import random

app = FastAPI()


router = APIRouter(prefix="/besumniiapi", tags=["bezumci"])

import time
from pathlib import Path
from fastapi import FastAPI
import cv2
import qrcode
import numpy as np
import json  # Заменим eval() на что-то менее страшное


SHARED_DIR = Path(__file__).parent.parent / "shared_qr"
print(SHARED_DIR.absolute())


# Функция декодирования QR через OpenCV и qreader
def decode_qr(image_path: Path):
    # Читаем изображение через OpenCV
    img = cv2.imread(str(image_path))
    # Используем qreader для декодирования
    from qreader import QReader

    qreader = QReader()
    decoded_text = qreader.detect_and_decode(image=img)
    return decoded_text[0] if decoded_text else None


@app.on_event("startup")
def start_scanning():
    import threading

    print("Запускаем AQRI")
    threading.Thread(target=process_requests, daemon=True).start()


def process_requests():
    while True:
        requests_dir = SHARED_DIR / "requests"
        responses_dir = SHARED_DIR / "responses"

        for request_file in requests_dir.glob("request_*.png"):
            print("Проверка QR кода ", request_file)
            try:
                # Декодируем QR
                decoded_text = decode_qr(request_file)
                if not decoded_text:
                    continue

                # Парсим JSON (теперь без eval!)
                data = json.loads(decoded_text)
                print("Декодированные данные", data)

                match = re.search(r"request_(\d+)\.png", request_file.name)
                if match:
                    request_id = int(match.group(1))
                else:
                    request_id = 0
                response_data = f"Сервер получил: {data}"

                method = data["method"]
                if method == "GET":
                    notes = read_notes()
                    response_data = {"notes": notes}

                elif method == "POST":
                    body = data["body"]
                    text = body.get("text")
                    if not text:
                        raise Exception("Text required")
                    add_note(text)

                    notes = read_notes()
                    response_data = {"notes": notes}

                elif method == "DELETE":
                    body = data["body"]
                    index = body.get("index")
                    if index is None or not isinstance(index, int):
                        raise Exception(
                            "Index required and must be an integer",
                        )
                    if delete_note(index):
                        notes = read_notes()
                        response_data = {"notes": notes}
                    else:
                        raise Exception("Note not found")

                elif method == "PUT":
                    body = data["body"]
                    index = body.get("index")
                    new_text = body.get("new_text")
                    if index is None or not isinstance(index, int) or not new_text:
                        raise Exception("Index and new_text required")
                    if edit_note(index, new_text):
                        notes = read_notes()
                        response_data = {"notes": notes}
                    else:
                        raise Exception("Note not found")

                # Генерируем ответный QR
                qr = qrcode.make(response_data)
                response_path = responses_dir / f"response_{request_id}.png"
                qr.save(response_path)

                request_file.unlink()  # Удаляем запрос
            except Exception as e:
                print(f"Ошибка: {e}")

        time.sleep(10)


def read_notes() -> list[str]:
    if not os.path.exists("notes.txt"):
        return []
    with open("notes.txt", "r", encoding="utf-8") as f:
        return f.readlines()


def add_note(text: str) -> None:
    with open("notes.txt", "a", encoding="utf-8") as f:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {text}\n")


def delete_note(index: int) -> bool:
    notes = read_notes()
    if 0 <= index < len(notes):
        notes.pop(index)
        with open("notes.txt", "w", encoding="utf-8") as f:
            f.writelines(notes)
        return True
    return False


# Редактирование заметки по индексу
def edit_note(index: int, new_text: str) -> bool:
    notes = read_notes()
    if 0 <= index < len(notes):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        notes[index] = f"[{timestamp}] {new_text}\n"
        with open("notes.txt", "w", encoding="utf-8") as f:
            f.writelines(notes)
        return True
    return False


@app.route(
    "/офигетькакойкрутойэндпоинтвсенанемработает",
    methods=["GET", "POST", "DELETE", "PUT"],
)
async def samuiluchshiirouterbestever(request: Request):
    """Здесь не будет никакого описания, даже не думайте об этом"""
    method = request.method

    if method == "GET":
        notes = read_notes()
        return JSONResponse(content={"notes": notes})

    elif method == "POST":
        body = await request.json()
        text = body.get("text")
        if not text:
            raise HTTPException(status_code=400, detail="Text required")
        add_note(text)
        return JSONResponse(content={"success": True})

    elif method == "DELETE":
        body = await request.json()
        index = body.get("index")
        if index is None or not isinstance(index, int):
            raise HTTPException(
                status_code=400, detail="Index required and must be an integer"
            )
        if delete_note(index):
            return JSONResponse(content={"success": True})
        else:
            raise HTTPException(status_code=404, detail="Note not found")

    elif method == "PUT":
        body = await request.json()
        index = body.get("index")
        new_text = body.get("new_text")
        if index is None or not isinstance(index, int) or not new_text:
            raise HTTPException(status_code=400, detail="Index and new_text required")
        if edit_note(index, new_text):
            return JSONResponse(content={"success": True})
        else:
            raise HTTPException(status_code=404, detail="Note not found")

    else:
        raise HTTPException(status_code=405, detail="Method not allowed")
