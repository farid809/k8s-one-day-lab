# 5 · Exercise 4 — Helm (~30 min)

**Goal:** deploy the entire application — everything Exercise 2 built over
two hours — with one command. This exercise is short on purpose: the length
of each exercise today has tracked how much work the tooling does for you.

## 5.1 What Helm adds

Exercise 2 turned shell commands into ten declarative files. Helm packages
those files into a **chart**: one versioned, installable unit with its
variable parts (image tags, replica counts, credentials) extracted into a
single `values.yaml`. A running installation of a chart is a **release** —
something you can upgrade, roll back, and uninstall as a whole.

Look inside `chart/taskboard/`: the templates are the *same manifests* from
`k8s/`, with the tunable values replaced by `{{ .Values.… }}` placeholders.
Nothing new conceptually — just packaged.

## 5.2 Install Helm

```bash
brew install helm        # macOS
winget install Helm.Helm # Windows
```

## 5.3 Deploy the whole app in one command

Start clean, then install:

```bash
kubectl delete namespace taskboard   # remove the Exercise 2/3 installation
helm install taskboard chart/taskboard -n taskboard --create-namespace
kubectl get pods -n taskboard -w     # the full stack converges; Ctrl-C when Ready
minikube service gateway -n taskboard
```

That's the entire Exercise 2 sequence — namespace, secret, PVC, database,
API, gateway, services — in one command.

## 5.4 The release lifecycle

**Upgrade** (change a value, not a file):

```bash
helm upgrade taskboard chart/taskboard -n taskboard --set api.replicaCount=5
kubectl get pods -n taskboard        # five api pods
```

**Roll back** (one command, whole app):

```bash
helm history taskboard -n taskboard
helm rollback taskboard 1 -n taskboard
kubectl get pods -n taskboard        # back to two api pods
```

**A second environment** — the task that fell apart in Exercise 1:

```bash
helm install taskboard-stg chart/taskboard -n taskboard-stg --create-namespace
helm list --all-namespaces           # two releases, same chart
```

A complete, isolated staging copy: one command, zero edits.
Remove it: `helm uninstall taskboard-stg -n taskboard-stg && kubectl delete ns taskboard-stg`.

## 5.5 Where each layer earns its place

| Layer | You write | Good for |
|---|---|---|
| Docker | run commands | one container, local dev |
| Kubernetes manifests | declarative YAML per object | understanding and controlling every object |
| Helm chart | templates + one values file | installing/upgrading the whole app, many environments |

In practice teams consume most third-party software as charts
(`helm install prometheus …`) and package their own apps the same way.

## Wrap-up (whole group, ~15 min)

Three questions to close the day:

1. Which Exercise 1 limitation stood out most to you — and which Kubernetes
   object addressed it?
2. In scenario 3 of the troubleshooting exercise, every pod was green and the
   app was still down. What's the general lesson about "is it healthy?" vs
   "is it wired?"
3. Your real projects: which service would you containerize first — and would
   you hand your team the `k8s/` manifests, a chart, or both?

## Where to go next

- [Kubernetes Basics](https://kubernetes.io/docs/tutorials/kubernetes-basics/) — official interactive tutorial; good repetition of today
- [Killercoda scenarios](https://killercoda.com/kubernetes) — free browser playgrounds for more reps
- Ingress, StatefulSets, RBAC — the topics we deliberately skipped, in the order worth learning them

## Clean up (end of the lab day)

```bash
helm uninstall taskboard -n taskboard
kubectl delete namespace taskboard
minikube stop            # or: minikube delete (removes the VM entirely)
```
