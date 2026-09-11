# Kubernetes in One Day

A one-day hands-on lab covering container and Kubernetes fundamentals.
Participants containerize and run a three-tier web application with Docker,
convert it to Kubernetes (minikube) using Deployments, Services, and
persistent storage, and practice diagnosing and fixing common failures.

The lab is structured as a before/after comparison: Exercise 1 runs the
application with Docker commands alone, surfacing the operational
limitations of manual container management; Exercise 2 deploys the same
application and images on Kubernetes, mapping each limitation to the
Kubernetes object that addresses it; Exercise 3 covers troubleshooting
through five guided failure scenarios; Exercise 4 packages the whole
application as a Helm chart and redeploys it in one command.

The exercises get shorter as the day progresses — that is deliberate.
Exercise 1 takes three hours of manual work, Exercise 2 does more in two,
and Exercise 4 redeploys everything in thirty minutes. The declining effort
per result *is* the lesson.

## The app

A Task Board — three tiers, deliberately small:
**nginx gateway** → **FastAPI API** → **PostgreSQL** (with persistent storage).
Full tour in [docs/01-the-app.md](docs/01-the-app.md).

## Schedule

| Time | Block | Doc |
|------|-------|-----|
| before the day | Setup (~30 min, on your own) | [docs/00-setup.md](docs/00-setup.md) |
| 09:00 – 09:20 | The app — code walkthrough | [docs/01-the-app.md](docs/01-the-app.md) |
| 09:20 – 12:20 | **Exercise 1** (~3 h) — running the app with Docker | [docs/02-exercise-1-containers.md](docs/02-exercise-1-containers.md) |
| 12:20 – 13:00 | Lunch | |
| 13:00 – 15:00 | **Exercise 2** (~2 h) — the Kubernetes way (minikube, Deployments, Services, PVC) | [docs/03-exercise-2-kubernetes.md](docs/03-exercise-2-kubernetes.md) |
| 15:00 – 15:15 | Break | |
| 15:15 – 16:30 | **Exercise 3** (~1.25 h) — troubleshooting five real failures | [docs/04-exercise-3-troubleshooting.md](docs/04-exercise-3-troubleshooting.md) |
| 16:30 – 17:00 | **Exercise 4** (~30 min) — the whole app as a Helm chart | [docs/05-exercise-4-helm.md](docs/05-exercise-4-helm.md) |
| 17:00 – 17:15 | Wrap-up discussion | (end of exercise 4) |

## Repo map

```
app/              the Task Board — gateway (nginx), api (FastAPI), db (seed SQL)
k8s/              Kubernetes manifests, numbered in teaching order, commented
chart/            the same app packaged as a Helm chart (Exercise 4)
troubleshooting/  five broken.yaml + SOLUTION.md pairs for Exercise 3
docs/             the lab itself — read these in order
docs/diagrams/    draw.io sources (architecture, limitations→answers, object map)
```

## For instructors

- Exercises are self-paced; the docs are written to be followed without a
  presenter. Budget floating help for Exercise 1 §2.2 (the deliberate crash)
  and Exercise 3 scenario 3 (the sneaky one).
- The **limitation** markers in Exercise 1 and the limitation→answer table
  opening Exercise 2 are the narrative spine — keep referring back to them.
- Diagrams are draw.io files (open with the draw.io desktop app or
  [app.diagrams.net](https://app.diagrams.net)); the docs embed mermaid
  equivalents that render directly on GitHub/Bitbucket.
- No registry is needed: images are built locally and `minikube image load`ed.
- The exercise durations descend by design (3 h → 2 h → 1.25 h → 0.5 h);
  resist compressing Exercise 1 — the time spent there is what makes the
  later exercises land.
- Out of scope, on purpose: Ingress controllers, StatefulSets, RBAC,
  multi-node. Mentioned at the end as the next things to learn.
