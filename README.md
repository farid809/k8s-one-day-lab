# Kubernetes in One Day

A one-day hands-on lab covering container and Kubernetes fundamentals.
Participants containerize and run a three-tier web application with Docker,
convert it to Kubernetes (minikube) using Deployments, Services, and
persistent storage, and practice diagnosing and fixing common failures.

The lab is a before/after comparison: run the app with Docker commands
alone and hit the limitations of manual container management, then deploy
the same app on Kubernetes and see each limitation addressed by a named
object, then troubleshoot five guided failures, then redeploy the whole
thing with Helm in one command.

## The app

A Task Board — three tiers, deliberately small:
**nginx gateway** → **FastAPI API** → **PostgreSQL** (with persistent storage).
Full tour in [docs/01-the-app.md](docs/01-the-app.md).

## The exercises

| Block | Time | Doc |
|-------|------|-----|
| Setup (do this beforehand) | ~30 min | [docs/00-setup.md](docs/00-setup.md) |
| The app — code walkthrough | ~15 min | [docs/01-the-app.md](docs/01-the-app.md) |
| **Exercise 1** — running the app with Docker | ~1.5 h | [docs/02-exercise-1-containers.md](docs/02-exercise-1-containers.md) |
| **Exercise 2** — the Kubernetes way | ~2 h (the deploying itself is minutes — the time goes into understanding the objects) | [docs/03-exercise-2-kubernetes.md](docs/03-exercise-2-kubernetes.md) |
| **Exercise 3** — troubleshooting five real failures | ~1 h | [docs/04-exercise-3-troubleshooting.md](docs/04-exercise-3-troubleshooting.md) |
| **Exercise 4** — the whole app as a Helm chart | ~30 min | [docs/05-exercise-4-helm.md](docs/05-exercise-4-helm.md) |

## Repo map

```
app/              the Task Board — gateway (nginx), api (FastAPI), db (seed SQL)
k8s/              Kubernetes manifests, numbered in teaching order, commented
chart/            the same app packaged as a Helm chart (Exercise 4)
troubleshooting/  five broken.yaml + SOLUTION.md pairs for Exercise 3
docs/             the lab itself — read these in order
docs/diagrams/    diagrams — rendered PNGs (embedded in the docs) + editable draw.io sources
```

## Notes

- Exercises are self-paced — the docs are written to be followed on your own.
- No registry needed: images are built locally and `minikube image load`ed.
- Not covered (learn these next): Ingress controllers, StatefulSets, RBAC,
  multi-node clusters.
