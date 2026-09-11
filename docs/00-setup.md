# 0 · Setup (before the lab day, ~30 min)

Do this **before** the lab. If `minikube start` works on your machine, you're done.

## Install

| Tool | macOS | Windows |
|------|-------|---------|
| Docker Desktop | `brew install --cask docker` | [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/) |
| minikube | `brew install minikube` | `winget install Kubernetes.minikube` |
| kubectl | `brew install kubectl` | `winget install Kubernetes.kubectl` |
| Helm (used in Exercise 4) | `brew install helm` | `winget install Helm.Helm` |

> Linux: install Docker Engine from your distro, then minikube + kubectl per
> [minikube.sigs.k8s.io/docs/start](https://minikube.sigs.k8s.io/docs/start/).

## Verify

```bash
docker version          # Client and Server sections both print
docker run hello-world  # prints a welcome message

minikube start          # first run downloads ~1GB — do this on good wifi
kubectl get nodes       # one node, STATUS Ready
minikube stop           # we'll start it again in Exercise 2
```

## Get the lab

```bash
git clone https://github.com/farid809/k8s-one-day-lab.git k8s-one-day-lab
cd k8s-one-day-lab
```

## Troubles?

- **Docker daemon not running** — start Docker Desktop first; minikube uses it as its VM driver.
- **Corporate proxy** — Docker Desktop → Settings → Resources → Proxies; minikube needs `minikube start --docker-env HTTP_PROXY=...`.
- **Nothing works on your machine at all** — fallback: [killercoda.com/playgrounds/scenario/kubernetes](https://killercoda.com/playgrounds/scenario/kubernetes) gives you a throwaway cluster in the browser (sessions last ~1 hour; you'll re-clone the repo each session).

Next → [1 · The app](01-the-app.md)
