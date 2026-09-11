# Scenario 2 — Solution

**Symptom:** new api pods cycle `Running` → `Error` → `CrashLoopBackOff`, restart
count climbing.

**Diagnosis path:** `describe` shows the container exiting, but the Events don't
say *why the app* died — for that you need the app's own output:

```bash
kubectl get pods -n taskboard
kubectl logs -n taskboard <api-pod-name>            # current attempt
kubectl logs -n taskboard <api-pod-name> --previous # the attempt that crashed
```

The traceback ends with:

```
psycopg2.OperationalError: could not translate host name "database" to address
```

**Root cause:** `DB_HOST` is set to `database`, but the Service in front of
postgres is named `db`. Cluster DNS has no `database` record, the API fails
fast on startup (by design — no retry loop), Kubernetes restarts it, repeat.

**Fix:**

```bash
kubectl apply -f k8s/05-api-deployment.yaml
```

**Lesson:** `describe` is for *cluster* problems (scheduling, images, probes);
`logs` is for *application* problems. CrashLoopBackOff almost always means
"read the logs" — and `--previous` shows the crash you actually care about.
