"""Task Board API — the middle tier of the lab app.

Deliberately simple. One table, four endpoints, ~100 lines.

NOTE for lab authors: there is NO retry loop on the database connection.
That is intentional. In Exercise 1 it demonstrates the startup-ordering
problem with raw containers; in Exercise 2 it demonstrates Kubernetes
self-healing (CrashLoopBackOff -> Running once the DB is reachable).
"""

import os
import socket

import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DB_CONFIG = {
    "host": os.environ["DB_HOST"],
    "port": int(os.environ.get("DB_PORT", "5432")),
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
    "dbname": os.environ.get("DB_NAME", "taskboard"),
}

HOSTNAME = socket.gethostname()  # shows which container/pod answered

app = FastAPI(title="Task Board API")


def get_conn():
    return psycopg2.connect(**DB_CONFIG)


# Fail fast if the DB is unreachable at startup — see module docstring.
with get_conn() as conn, conn.cursor() as cur:
    cur.execute(
        """CREATE TABLE IF NOT EXISTS tasks (
               id SERIAL PRIMARY KEY,
               title TEXT NOT NULL,
               done BOOLEAN NOT NULL DEFAULT FALSE
           )"""
    )
    conn.commit()


class TaskIn(BaseModel):
    title: str


@app.get("/healthz")
def healthz():
    """Liveness: the process is up."""
    return {"status": "ok", "served_by": HOSTNAME}


@app.get("/readyz")
def readyz():
    """Readiness: we can actually reach the database."""
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT 1")
    except Exception:
        raise HTTPException(status_code=503, detail="database unreachable")
    return {"status": "ready", "served_by": HOSTNAME}


@app.get("/tasks")
def list_tasks():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT id, title, done FROM tasks ORDER BY id")
        rows = cur.fetchall()
    return {
        "served_by": HOSTNAME,
        "tasks": [{"id": r[0], "title": r[1], "done": r[2]} for r in rows],
    }


@app.post("/tasks", status_code=201)
def create_task(task: TaskIn):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("INSERT INTO tasks (title) VALUES (%s) RETURNING id", (task.title,))
        task_id = cur.fetchone()[0]
        conn.commit()
    return {"id": task_id, "title": task.title, "done": False, "served_by": HOSTNAME}


@app.put("/tasks/{task_id}/toggle")
def toggle_task(task_id: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("UPDATE tasks SET done = NOT done WHERE id = %s RETURNING done", (task_id,))
        row = cur.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="no such task")
        conn.commit()
    return {"id": task_id, "done": row[0], "served_by": HOSTNAME}


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        conn.commit()
