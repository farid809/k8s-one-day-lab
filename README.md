# Kubernetes in One Day

A hands-on lab that takes a developer from "I've heard of containers" to
running, scaling, and troubleshooting a real three-tier app on Kubernetes —
in one working day.

**The premise:** you can't appreciate Kubernetes until you've been the
orchestrator yourself. So first you run the app with raw `docker` commands
and hit five specific pains, by design. Then you run the *same app, same
images* on Kubernetes and watch each pain get absorbed by a named object.
Then you break it five ways and learn the diagnosis loop.

## The app

A Task Board — three tiers, deliberately small:
**nginx gateway** → **FastAPI API** → **PostgreSQL** (with persistent storage).
Full tour in [docs/01-the-app.md](docs/01-the-app.md).

## Schedule

| Time | Block | Doc |
|------|-------|-----|
| before the day | Setup (~30 min, on your own) | [docs/00-setup.md](docs/00-setup.md) |
| 09:00 – 09:20 | The app — code walkthrough | [docs/01-the-app.md](docs/01-the-app.md) |
| 09:20 – 11:20 | **Exercise 1** — containers by hand (feel the pain) | [docs/02-exercise-1-containers.md](docs/02-exercise-1-containers.md) |
| 11:30 – 14:30 | **Exercise 2** — the Kubernetes way (minikube, Deployments, Services, PVC) | [docs/03-exercise-2-kubernetes.md](docs/03-exercise-2-kubernetes.md) |
| 14:45 – 16:15 | **Exercise 3** — troubleshooting five real failures | [docs/04-exercise-3-troubleshooting.md](docs/04-exercise-3-troubleshooting.md) |
| 16:15 – 16:30 | Wrap-up discussion | (end of exercise 3) |

## Repo map

```
app/              the Task Board — gateway (nginx), api (FastAPI), db (seed SQL)
k8s/              Kubernetes manifests, numbered in teaching order, commented
troubleshooting/  five broken.yaml + SOLUTION.md pairs for Exercise 3
docs/             the lab itself — read these in order
docs/diagrams/    draw.io sources (architecture, pains→answers, object map)
```

## For instructors

- Exercises are self-paced; the docs are written to be followed without a
  presenter. Budget floating help for Exercise 1 §2.2 (the deliberate crash)
  and Exercise 3 scenario 3 (the sneaky one).
- The ⚡ **pain** markers in Exercise 1 and the pain→answer table opening
  Exercise 2 are the narrative spine — keep referring back to them.
- Diagrams are draw.io files (open with the draw.io desktop app or
  [app.diagrams.net](https://app.diagrams.net)); the docs embed mermaid
  equivalents that render directly on GitHub/Bitbucket.
- No registry is needed: images are built locally and `minikube image load`ed.
- Out of scope, on purpose: Helm, Ingress controllers, StatefulSets, RBAC,
  multi-node. Mentioned at the end as the next things to learn.
