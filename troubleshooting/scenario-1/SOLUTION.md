# Scenario 1 — Solution

**Symptom:** `kubectl get pods -n taskboard` shows the new postgres pod stuck in
`ErrImagePull` / `ImagePullBackOff`. The old pod may still be running (a Deployment
keeps the old ReplicaSet up until the new one is Ready — that's rolling updates
protecting you, and it's worth pointing out).

**Diagnosis path:**

```bash
kubectl get pods -n taskboard                      # spot the state
kubectl describe pod -n taskboard -l app=postgres  # read the Events section
```

Events say it plainly:

```
Failed to pull image "postgres:16-alpin": ... not found
```

**Root cause:** image tag typo — `postgres:16-alpin` instead of `postgres:16-alpine`.
The registry has no such tag, the kubelet retries with backoff, hence
`ImagePullBackOff`.

**Fix — reapply the known-good manifest:**

```bash
kubectl apply -f k8s/03-postgres-deployment.yaml
kubectl get pods -n taskboard -w
```

**Lesson:** `describe` + the Events section answers most "why is my pod not
running" questions. And because desired state lives in files, recovery is
re-applying the good file — not surgery on the cluster.
