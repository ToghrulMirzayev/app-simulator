FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install fastapi psycopg2-binary uvicorn jinja2

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]