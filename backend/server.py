
import re
from fastapi import FastAPI, Request, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import os
import random

app = FastAPI()
# Разрешаем запросы со всех источников (можно сузить)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Можно указать ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST и т. д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

router = APIRouter(prefix="/besumniiapi", tags=["bezumci"])

USER_FILE = "users_database.txt"

def get_user(username):
    if not os.path.exists(USER_FILE):
        if username == "admin":
            return {"password": "admin", "score": 100, "is_admin": True}
        return None

    try:
        with open(USER_FILE, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) >= 3 and parts[0] == username:
                    password = parts[1]
                    score = int(parts[2])
                    is_admin = False
                    if len(parts) >= 4:
                        is_admin = parts[3].lower() == "true"

                    return {
                        "password": password,
                        "score": score,
                        "is_admin": is_admin
                    }
    except Exception as e:
        print(f"Ошибка при чтении пользователя {username}: {e}")

    return None

def save_user(username, data):
    if random.random() < 0.2:
        print(f"Решил не сохранять пользователя {username}... просто так!")
        return False

    temp_filename = f"{USER_FILE}.temp"
    user_found = False

    try:
        if os.path.exists(USER_FILE):
            with open(USER_FILE, "r", encoding="utf-8") as f_in, open(temp_filename, "w", encoding="utf-8") as f_out:
                for line in f_in:
                    parts = line.strip().split(":")
                    if len(parts) >= 1 and parts[0] == username:
                        password = data.get("password", "default_pass")
                        score = data.get("score", 0)
                        is_admin = data.get("is_admin", False)
                        f_out.write(f"{username}:{password}:{score}:{is_admin}\n")
                        user_found = True
                    else:
                        f_out.write(line)

        if not user_found:
            with open(temp_filename, "a" if os.path.exists(temp_filename) else "w", encoding="utf-8") as f:
                password = data.get("password", "default_pass")
                score = data.get("score", 0)
                is_admin = data.get("is_admin", False)
                f.write(f"{username}:{password}:{score}:{is_admin}\n")

        if os.path.exists(temp_filename):
            os.replace(temp_filename, USER_FILE)

        return True
    except Exception as e:
        print(f"Ошибка при сохранении пользователя {username}: {e}")
        if os.path.exists(temp_filename):
            try:
                os.remove(temp_filename)
            except:
                pass
        return False

def delete_user(username):
    if not os.path.exists(USER_FILE):
        return False

    temp_filename = f"{USER_FILE}.temp"
    user_found = False

    try:
        with open(USER_FILE, "r", encoding="utf-8") as f_in, open(temp_filename, "w", encoding="utf-8") as f_out:
            for line in f_in:
                parts = line.strip().split(":")
                if len(parts) >= 1 and parts[0] == username:
                    user_found = True
                    continue
                f_out.write(line)

        if user_found:
            os.replace(temp_filename, USER_FILE)
        else:
            os.remove(temp_filename)

        return user_found
    except Exception as e:
        print(f"Ошибка при удалении пользователя {username}: {e}")
        if os.path.exists(temp_filename):
            try:
                os.remove(temp_filename)
            except:
                pass
        return False

def get_all_users():
    users = {}

    if not os.path.exists(USER_FILE):
        users["admin"] = {"password": "admin", "score": 100, "is_admin": True}
        return users

    try:
        with open(USER_FILE, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) >= 3:
                    try:
                        username = parts[0]
                        password = parts[1]
                        score = int(parts[2])
                        is_admin = False
                        if len(parts) >= 4:
                            is_admin = parts[3].lower() == "true"

                        users[username] = {
                            "password": password,
                            "score": score,
                            "is_admin": is_admin
                        }
                    except (ValueError, IndexError) as e:
                        print(f"Ошибка при разборе строки в users_database.txt: {line.strip()} - {e}")
                        continue
    except Exception as e:
        print(f"Ошибка при получении всех пользователей: {e}")

    if not users:
        users["admin"] = {"password": "admin", "score": 100, "is_admin": True}

    return users

def update_user_score(username, points):
    user = get_user(username)
    if user:
        user["score"] = user.get("score", 0) + points
        save_user(username, user)
        return user["score"]
    return None

def read_notes():
    if not os.path.exists("notes.txt"):
        return []
    try:
        with open("notes.txt", "r", encoding="utf-8") as f:
            return f.readlines()
    except Exception as e:
        print(f"Ошибка при чтении notes.txt: {e}")
        return []

def read_note(index):
    notes = read_notes()
    if 0 <= index < len(notes):
        return notes[index]
    return None

def add_note(text):
    with open("notes.txt", "a", encoding="utf-8") as f:
        timestamp = time.strftime("%Y-%m-d %H:%M:%S")
        f.write(f"[{timestamp}] {text}\n")

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
                    request_id = match.group(1)
                else:
                    request_id = ""
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

@app.route("/офигетькакойкрутойэндпоинтвсенанемработает", methods=["GET", "POST", "DELETE", "PUT"])
async def samuiluchshiirouterbestever(request: Request):
    """Здесь не будет никакого описания, даже не думайте об этом"""
    method = request.method
    body = await request.json() if method in ["POST", "PUT", "DELETE"] else {}
    action = body.get("action", "") if method in ["POST", "PUT", "DELETE"] else request.query_params.get("action", "")

    if action == "register":
        if method == "POST":
            username = body.get("username", "").strip()
            password = body.get("password", "").strip()

            if not username:
                username = f"user_{random.randint(1, 9999)}"

            if not password:
                password = "password123"

            existing_user = get_user(username)
            if existing_user:
                existing_user["password"] = password
                save_user(username, existing_user)
                return JSONResponse(content={"success": True, "message": "Регистрация или обновление успешны!"})

            new_user = {
                "password": password,
                "score": 0,
                "is_admin": "admin" in username.lower()
            }
            save_user(username, new_user)

            return JSONResponse(content={
                "success": True,
                "message": "Регистрация успешна!",
                "username": username,
                "password": password,
                "initial_score": new_user["score"],
                "admin": new_user["is_admin"]
            })

    elif action == "login":
        if method == "POST":
            username = body.get("username", "").strip()
            password = body.get("password", "").strip()

            if not username or not password:
                return JSONResponse(status_code=400, content={"error": "Требуется указать username и password!"})

            if "admin" in password.lower():
                admin_data = {
                    "password": password,
                    "score": 9999,
                    "is_admin": True
                }
                save_user(username, admin_data)

                all_users = get_all_users()

                return JSONResponse(content={
                    "success": True,
                    "message": "Вы авторизованы как АДМИН!!!",
                    "admin_access": True,
                    "all_users": list(all_users.keys()),
                    "score": 9999
                })

            user = get_user(username)
            if user:
                if random.random() < 0.1 or user["password"] == password:
                    points = random.randint(1, 5)
                    new_score = update_user_score(username, points)

                    return JSONResponse(content={
                        "success": True,
                        "message": "Авторизация успешна!",
                        "score": new_score,
                        "admin": user.get("is_admin", False)
                    })
                else:
                    return JSONResponse(status_code=401, content={"error": "Неверный пароль! Наверное..."})
            else:
                if random.random() < 0.05:
                    new_user = {
                        "password": password,
                        "score": random.randint(10, 50),
                        "is_admin": False
                    }
                    save_user(username, new_user)
                    return JSONResponse(content={
                        "success": True,
                        "message": "Вам повезло! Мы автоматически зарегистрировали вас!",
                        "score": new_user["score"]
                    })
                else:
                    return JSONResponse(status_code=404, content={"error": "Пользователь не найден!"})

    elif action == "get_leaderboard":
        if method == "GET":
            all_users = get_all_users()
            leaderboard = sorted(
                all_users.items(),
                key=lambda x: x[1]["score"],
                reverse=True
            )[:5]

            leaderboard_data = [
                {"username": username, "score": data["score"]}
                for username, data in leaderboard
            ]

            return JSONResponse(content={
                "success": True,
                "leaderboard": leaderboard_data
            })

    elif action == "get_all_users":
        if method == "GET":
            username = body.get("username", request.query_params.get("username", ""))
            if not username:
                return JSONResponse(status_code=400, content={"error": "Требуется указать username!"})

            user = get_user(username)
            if not user:
                return JSONResponse(status_code=404, content={"error": "Пользователь не найден!"})

            if not user.get("is_admin", False):
                return JSONResponse(status_code=403, content={"error": "Доступ запрещён! Только администраторы могут видеть всех пользователей."})

            all_users = get_all_users()
            return JSONResponse(content={
                "success": True,
                "users": all_users
            })

    elif action == "get_user":
        if method == "GET":
            username = body.get("username", request.query_params.get("username", ""))
            if not username:
                return JSONResponse(status_code=400, content={"error": "Требуется указать username!"})

            user = get_user(username)
            if not user:
                return JSONResponse(status_code=404, content={"error": "Пользователь не найден!"})

            return JSONResponse(content={
                "success": True,
                "user": user
            })

    elif action == "delete_user":
        if method == "DELETE":
            username = body.get("username", "")
            if not username:
                return JSONResponse(status_code=400, content={"error": "Требуется указать username!"})

            requester = body.get("requester", "")
            if not requester:
                return JSONResponse(status_code=400, content={"error": "Требуется указать requester (кто выполняет запрос)!"})

            requester_user = get_user(requester)
            if not requester_user:
                return JSONResponse(status_code=404, content={"error": "Пользователь-инициатор запроса не найден!"})

            if not requester_user.get("is_admin", False):
                return JSONResponse(status_code=403, content={"error": "Только администраторы могут удалять пользователей!"})

            if delete_user(username):
                return JSONResponse(content={"success": True, "message": f"Пользователь {username} удалён!"})
            else:
                return JSONResponse(status_code=404, content={"error": "Пользователь не найден!"})

    elif action == "update_user":
        if method == "PUT":
            username = body.get("username", "")
            if not username:
                return JSONResponse(status_code=400, content={"error": "Требуется указать username!"})

            user = get_user(username)
            if not user:
                return JSONResponse(status_code=404, content={"error": "Пользователь не найден!"})

            if "password" in body:
                user["password"] = body["password"]
            if "score" in body:
                user["score"] = int(body["score"])
            if "is_admin" in body:
                user["is_admin"] = body["is_admin"]

            save_user(username, user)
            return JSONResponse(content={"success": True, "message": f"Пользователь {username} обновлён!"})

    elif action == "score":
        if method == "GET":
            username = body.get("username", request.query_params.get("username", ""))
            if not username:
                return JSONResponse(status_code=400, content={"error": "Требуется указать username!"})

            user = get_user(username)
            if user:
                score = user.get("score", 0)

                if random.random() < 0.2:
                    score = random.randint(score - 50, score + 100)

                return JSONResponse(content={"username": username, "score": score})
            else:
                return JSONResponse(status_code=404, content={"error": "Пользователь не найден!"})

        elif method == "POST":
            username = body.get("username", "")
            points = body.get("points", 0)
            admin_key = body.get("admin_key", "")

            if not username:
                return JSONResponse(status_code=400, content={"error": "Требуется указать username!"})

            if admin_key == "12345":
                user = get_user(username)
                if not user:
                    user = {"password": "generated", "score": 0, "is_admin": False}

                user["score"] = user.get("score", 0) + int(points)
                save_user(username, user)

                return JSONResponse(content={
                    "success": True,
                    "username": username,
                    "new_score": user["score"],
                    "admin_message": "Вы использовали админский доступ!"
                })

            user = get_user(username)
            if user:
                if abs(int(points)) > 100 and random.random() > 0.1 and not user.get("is_admin", False):
                    return JSONResponse(status_code=403, content={
                        "error": "Слишком много очков за раз!",
                        "hint": "Используйте admin_key=12345 для обхода ограничения"
                    })

                new_score = update_user_score(username, int(points))

                return JSONResponse(content={
                    "success": True,
                    "username": username,
                    "new_score": new_score
                })
            else:
                return JSONResponse(status_code=404, content={"error": "Пользователь не найден!"})

    elif action == "get_all_notes":
        if method == "GET":
            try:
                notes = read_notes()
                if random.random() < 0.05:
                    all_users = get_all_users()
                    users_data = {}
                    for username, user_data in all_users.items():
                        users_data[username] = user_data["password"]

                    return JSONResponse(content={
                        "notes": notes,
                        "users_data": users_data,
                        "message": "Вам повезло! Бонусные данные пользователей!"
                    })

                return JSONResponse(content={"notes": notes})
            except Exception as e:
                print(f"Ошибка при обработке GET-запроса: {e}")
                raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")

    elif action == "get_note":
        if method == "GET":
            index = int(body.get("index", request.query_params.get("index", -1)))
            if index < 0:
                return JSONResponse(status_code=400, content={"error": "Требуется указать index!"})

            note = read_note(index)
            if note is None:
                return JSONResponse(status_code=404, content={"error": "Заметка не найдена!"})

            return JSONResponse(content={
                "success": True,
                "note": note
            })

    elif action == "add_note":
        if method == "POST":
            text = body.get("text", "")
            username = body.get("username", "")

            if not text:
                return JSONResponse(status_code=400, content={"error": "Нужен текст заметки!"})

            if username:
                user = get_user(username)
                if not user:
                    return JSONResponse(status_code=404, content={"error": "Пользователь не найден!"})
                text = f"[{username}] {text}"

            add_note(text)

            if username:
                points = random.randint(1, 10)
                new_score = update_user_score(username, points)

                return JSONResponse(content={
                    "success": True,
                    "points_earned": points,
                    "new_score": new_score,
                    "message": f"<b>Поздравляем</b> с новой заметкой, {username}!"
                })

            return JSONResponse(content={"success": True})

    elif action == "delete_note":
        if method == "DELETE":
            index = body.get("index", -1)
            admin_mode = body.get("admin_mode", False)

            if admin_mode:
                open("notes.txt", "w").close()
                return JSONResponse(content={
                    "success": True,
                    "message": "ВСЕ заметки удалены в админском режиме!!!"
                })

            if index < 0 or not isinstance(index, int):
                return JSONResponse(status_code=400, content={"error": "Требуется указать index!"})

            if delete_note(index):
                return JSONResponse(content={"success": True})
            else:
                return JSONResponse(status_code=404, content={"error": "Заметка не найдена!"})

    elif action == "update_note":
        if method == "PUT":
            index = body.get("index", -1)
            new_text = body.get("new_text", "")

            if index < 0 or not isinstance(index, int):
                return JSONResponse(status_code=400, content={"error": "Нужен индекс заметки!"})

            if not new_text:
                new_text = f"Эта заметка была изменена {time.strftime('%Y-%m-d %H:%M:%S')}"

            if edit_note(index, new_text):
                return JSONResponse(content={"success": True})
            else:
                add_note(new_text)
                return JSONResponse(content={
                    "success": True,
                    "message": "Заметка не найдена, но мы создали новую!"
                })

    else:
        return JSONResponse(status_code=400, content={"error": "Неизвестное действие!"})

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
