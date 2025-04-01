from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import time
import os
import random

app = FastAPI()


# Чтение заметок
def read_notes() -> list[str]:
    if not os.path.exists("notes.txt"):
        return []
    with open("notes.txt", "r", encoding="utf-8") as f:
        return f.readlines()


# Добавление заметки
def add_note(text: str) -> None:
    # "Безумная" фича: автозамена текста
    replacements = {
        "работа": "похер",
        "завтра": "никогда",
        "привет": "кек_лол_арара"
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    # "Безумная" фича: случайное удаление заметки
    if random.random() < 0.1:  # 10% шанс
        with open("notes.txt", "w", encoding="utf-8") as f:
            f.write("[SYSTEM] Я украл одну заметку, ха-ха!\n")
        return

    with open("notes.txt", "a", encoding="utf-8") as f:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {text}\n")


# Удаление заметки по индексу
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


# Единый эндпоинт для всех операций
@app.route("/офигетькакойкрутойэндпоинтвсенанемработает", methods=["GET", "POST", "DELETE", "PUT"])
async def samuiluchshiirouterbestever(request: Request):
    """Здесь не будет никакого описания, даже не думайте об этом"""
    method = request.method

    # GET: Получение заметок
    if method == "GET":
        notes = read_notes()
        # "Безумная" фича: случайная ошибка
        if random.random() < 0.1:  # 10% шанс
            raise HTTPException(status_code=500, detail="Сервер устал, попробуй позже")
        return JSONResponse(content={"notes": notes})

    # POST: Добавление заметки
    elif method == "POST":
        body = await request.json()
        text = body.get("text")
        if not text:
            raise HTTPException(status_code=400, detail="Text required")
        add_note(text)
        return JSONResponse(content={"success": True})

    # DELETE: Удаление заметки
    elif method == "DELETE":
        body = await request.json()
        index = body.get("index")
        if index is None or not isinstance(index, int):
            raise HTTPException(status_code=400, detail="Index required and must be an integer")
        if delete_note(index):
            return JSONResponse(content={"success": True})
        else:
            raise HTTPException(status_code=404, detail="Note not found")

    # PUT: Редактирование заметки
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