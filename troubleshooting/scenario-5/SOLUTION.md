# Scenario 5 — Solution

**Symptom:** UI is down (502), and `kubectl get pods -n taskboard` shows the new
api pods `Running` — but look closely at the READY column:

```
NAME                   READY   STATUS    RESTARTS
api-7d9f…              0/1     Running   0
api-8c2a…              0/1     Running   0
```

`Running` with `0/1 Ready`, zero restarts. Meanwhile the *old* pods are gone —
wait, are they? Actually no: check `kubectl get pods` again — the rollout is
**stuck**: the Deployment won't kill the last old pod until a new one is Ready,
and none ever is. (If you applied scenario 2 or 3 earlier and fixed them, you've
seen the healthy version of this protection.)

**Diagnosis path:**

```bash
kubectl describe pod -n taskboard <new-api-pod>
```

Events, repeating every 5 seconds:

```
Readiness probe failed: Get "http://10.244…:8080/readyz": connection refused
```

**Root cause:** the readiness probe points at port **8080**; the app listens on
**8000**. The probe fails, so the pod is never marked Ready, so the Service
never sends it traffic, so the rollout never completes.

Why no restarts? Because it's the *readiness* probe, not the *liveness* probe:

- **liveness fails** → container is killed and restarted ("it's dead, reboot it")
- **readiness fails** → pod just gets no traffic ("it's alive, but not ready to serve")

**Fix:**

```bash
kubectl apply -f k8s/05-api-deployment.yaml
kubectl rollout status deployment/api -n taskboard
```

**Lesson:** `Running` is about the process; `Ready` is about serving traffic.
Always read both columns — and know which probe does what, because the two
failure modes look completely different.
