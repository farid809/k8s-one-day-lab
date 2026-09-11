# 2 · Exercise 1 — Containers by hand (~1.5 h)

**Goal:** run the whole app with nothing but `docker` commands, and note
exactly where that approach stops scaling. Each limitation you encounter here
corresponds to a Kubernetes feature covered in Exercise 2. They are marked
like this:

> **Limitation #n — name.** What just happened, and why it doesn't scale.

Work from the repo root. If Docker Desktop isn't running, start it.

## 2.1 Build the images

```bash
docker build -t taskboard-api:v1 app/api
docker build -t taskboard-gateway:v1 app/gateway
docker images | grep taskboard
```

Read each Dockerfile as it builds — they're short and commented. Rebuild the
API image a second time: instant, because layers cache. That's the mechanic
that makes containers fast to iterate on.

(The database needs no build — the official `postgres:16-alpine` image is fine.)

## 2.2 First try: just run them

```bash
docker run -d --name api \
  -e DB_HOST=db -e DB_USER=taskboard -e DB_PASSWORD=lab-only-password \
  taskboard-api:v1

docker ps          # ...where is it?
docker ps -a       # Exited (1)
docker logs api    # psycopg2.OperationalError: could not translate host name "db"
```

> **Limitation #1 — startup order is your problem.** The API needs the DB first,
> and *you* have to know that and sequence it. Nothing restarts the failed
> container or retries later. In a 3-component app you can keep the order in
> your head. In a 30-component system, you can't.

```bash
docker rm api      # clean up the corpse — also your job
```

## 2.3 Do it properly: network, volume, then containers in order

Containers get isolated network stacks; to talk by name they need a shared
Docker network. Data needs a named volume. Both are created by hand:

```bash
docker network create taskboard-net
docker volume create taskboard-data
```

Now the DB — note the seed file mounted in, and the volume:

```bash
docker run -d --name db --network taskboard-net \
  -e POSTGRES_USER=taskboard -e POSTGRES_PASSWORD=lab-only-password -e POSTGRES_DB=taskboard \
  -v taskboard-data:/var/lib/postgresql/data \
  -v "$(pwd)/app/db/init.sql":/docker-entrypoint-initdb.d/init.sql:ro \
  postgres:16-alpine

docker logs -f db    # wait for "database system is ready to accept connections", Ctrl-C
```

Then the API and the gateway:

```bash
docker run -d --name api --network taskboard-net \
  -e DB_HOST=db -e DB_USER=taskboard -e DB_PASSWORD=lab-only-password \
  taskboard-api:v1

docker run -d --name gateway --network taskboard-net -p 8080:80 taskboard-gateway:v1
```

Open **http://localhost:8080** — the Task Board is up, seeded with tasks. Add
one. It works! Congratulations, you are now a human orchestrator.

> **Limitation #2 — the wiring lives in your shell history.** Count what you just
> typed: 1 network, 1 volume, 3 runs, ~10 `-e`/`-v`/`-p` flags, a password in
> plain text, in the right order. None of it is written down anywhere except
> your terminal. The next person gets it by asking you.

## 2.4 Test the limitations

**Kill the API** (pretend it crashed at 2am):

```bash
docker kill api
```

Refresh the browser — broken. Wait a minute — still broken. Nothing is coming
to help.

```bash
docker start api    # you are the healing mechanism
```

> **Limitation #3 — nothing restarts anything.** `docker run --restart=always`
> exists, but it's per-container, set at run time, and there's still no notion
> of "the app" as a whole — no health checks, no "don't send traffic until
> it's actually ready".

**Try to scale the API** (pretend load doubled):

```bash
docker run -d --name api-2 --network taskboard-net \
  -e DB_HOST=db -e DB_USER=taskboard -e DB_PASSWORD=lab-only-password \
  taskboard-api:v1
```

It runs — but check the UI's "served by" line while refreshing: always the
same hostname. `api-2` gets zero traffic. nginx proxies to `api`, singular.
To actually load-balance you'd edit `nginx.conf`, add an upstream block with
both names, rebuild the gateway image, and restart it. And repeat all that
when you add `api-3` or remove `api-2`.

> **Limitation #4 — scaling is a config-surgery project.** Adding a copy of a
> stateless service should be trivial. Here it means editing another
> component's config and rebuilding an image.

```bash
docker rm -f api-2   # abandon that idea
```

**Prove the data survives** (the volume payoff — this one actually works):

```bash
docker rm -f db
# recreate with the SAME docker run command as 2.3 (scroll up / history)
```

Refresh: tasks still there — they lived in `taskboard-data`, not the container.
Now the counterfactual — remove the `-v taskboard-data:...` flag and recreate
`db` again: fresh seeds, your added tasks gone. (Recreate it *with* the volume
before moving on.)

> **Limitation #5 — state is one forgotten flag from gone.** The difference
> between "data survives" and "data doesn't" was one `-v` in a command
> you typed by hand.

**Ship an update** (a routine release):

Edit `app/gateway/static/index.html` — change the `<h1>` from `Task Board`
to `Task Board v2`. Now get that change to "production":

```bash
docker build -t taskboard-gateway:v2 app/gateway
docker rm -f gateway            # the app's front door is now DOWN
docker run -d --name gateway --network taskboard-net -p 8080:80 taskboard-gateway:v2
```

Keep refreshing the browser while you do it: between the `rm` and the new
container becoming ready, every user gets a connection error. To avoid that
window you'd need a second gateway, a load balancer in front, health checks,
and a scripted cutover — for a one-line HTML change.

If the release is bad, rolling back is the same manual sequence in reverse,
under pressure.

> **Limitation #6 — every update means downtime.** Replacing a container is
> stop-then-start. Zero-downtime deploys and instant rollbacks are an
> infrastructure project you'd have to build yourself.

**A second environment?** (thought experiment, no typing needed):

Say QA asks for a staging copy. Everything you built is named and wired by
hand, so a second copy means repeating every command with `-stg` names, a
different port — and the gateway can't even join as-is, because its
nginx.conf proxies to `api`, not `api-stg`. That's a config edit and an
image rebuild, for a *copy*. And the two copies start drifting the moment
they exist.

> **Limitation #7 — a second environment means doing everything again.**
> There is no "copy of the whole app" concept — only individual containers
> recreated by hand, with names adjusted everywhere they're referenced.

## 2.5 Summary: what manual orchestration costs

For **one** small app on **one** machine you personally manage: build order,
startup order, a network, a volume, port mappings, plaintext secrets, restarts,
a scaling approach that requires image rebuilds, downtime on every release,
and a full manual rebuild for each additional environment. Multiply by 30
services, 3 environments, and a 2am pager.

The fix isn't more discipline. It's declaring the desired state and letting
software converge on it. That's Exercise 2.

## 2.6 Clean up (everything goes — we rebuild it the K8s way)

```bash
docker rm -f gateway api db
docker network rm taskboard-net
docker volume rm taskboard-data
git checkout -- app/gateway/static/index.html   # undo the v2 heading edit
```

Next → [3 · Exercise 2: the Kubernetes way](03-exercise-2-kubernetes.md)
