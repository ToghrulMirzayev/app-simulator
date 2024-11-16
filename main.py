from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.responses import JSONResponse
import psycopg2

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_status_from_db():
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="db",
        port="5432"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT status_value FROM config LIMIT 1;")
    status_value = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return status_value

def get_update_enabled_from_db():
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="db",
        port="5432"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT is_update_enabled FROM config LIMIT 1;")
    is_update_enabled = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return is_update_enabled

def get_language_from_db():
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="db",
        port="5432"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT language FROM language_config LIMIT 1;")
    language = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return language

def get_phrase_of_the_day_from_db():
    language = get_language_from_db()
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="db",
        port="5432"
    )
    cursor = connection.cursor()
    
    if language == "RU":
        cursor.execute("SELECT ru_text FROM phrases WHERE ru_text IS NOT NULL ORDER BY RANDOM() LIMIT 1;")
    else:
        cursor.execute("SELECT en_text FROM phrases WHERE en_text IS NOT NULL ORDER BY RANDOM() LIMIT 1;")
    
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if result is None:
        return "Нет доступных фраз."
    return result[0]

def update_status_in_db(new_status_value: int):
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="db",
        port="5432"
    )
    cursor = connection.cursor()
    cursor.execute("UPDATE config SET status_value = %s WHERE id = 1;", (new_status_value,))
    connection.commit()
    cursor.close()
    connection.close()

class StatusUpdate(BaseModel):
    status: int

@app.get("/")
async def read_root(request: Request):
    is_update_enabled = get_update_enabled_from_db()
    phrase_of_the_day = get_phrase_of_the_day_from_db()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "is_update_enabled": is_update_enabled,
        "phrase_of_the_day": phrase_of_the_day
    })

@app.get("/api/status")
async def get_status():
    status_value = get_status_from_db()
    if status_value > 80:
        status = "HEALTHY"
    elif status_value > 20:
        status = "WARNING"
    else:
        status = "BAD"
    return JSONResponse({"status": status})

@app.get("/api/update-enabled")
async def get_update_enabled():
    is_update_enabled = get_update_enabled_from_db()
    return JSONResponse({"is_update_enabled": is_update_enabled})

@app.post("/api/status")
async def update_status(status_update: StatusUpdate):
    new_status_value = status_update.status
    update_status_in_db(new_status_value)
    return JSONResponse({"message": "Status updated successfully"})

@app.get("/api/phrase-of-the-day")
async def get_phrase_of_the_day():
    phrase = get_phrase_of_the_day_from_db()
    return JSONResponse({"phrase_of_the_day": phrase})
