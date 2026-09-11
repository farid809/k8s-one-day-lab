# Task Board API — python base, deps, code, run. Four moves.
FROM python:3.12-slim

WORKDIR /app

# Copy requirements first so Docker caches the (slow) pip install layer
# and only re-runs it when requirements.txt changes — not on every code edit.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
