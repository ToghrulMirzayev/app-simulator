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
    return templates.TemplateResponse("index.html", {"request": request})

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

@app.post("/api/status")
async def update_status(status_update: StatusUpdate):
    new_status_value = status_update.status
    update_status_in_db(new_status_value)
    return JSONResponse({"message": "Status updated successfully"})
