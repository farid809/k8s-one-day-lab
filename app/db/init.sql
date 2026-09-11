-- Seed data. The official postgres image runs any .sql in
-- /docker-entrypoint-initdb.d/ on FIRST startup of an empty data directory —
-- which is exactly the behavior the storage exercises poke at: wipe the
-- volume, seeds come back; keep the volume, your data survives.
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE
);

INSERT INTO tasks (title, done) VALUES
    ('Finish Exercise 1 — containers by hand', false),
    ('Review the app architecture', false),
    ('Finish Exercise 2 — the Kubernetes way', false),
    ('Break things on purpose in Exercise 3', false);
