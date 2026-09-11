# Scenario 3 — Solution

**Symptom:** the sneaky one. Every pod is `Running` and `Ready`. No events, no
crashes, nothing red anywhere — but the UI shows **502 Bad Gateway** and
`kubectl logs` on the gateway shows `api could not be resolved` /
`connect() failed`.

**Diagnosis path:** when pods are healthy but traffic doesn't arrive, suspect
the wiring between Service and pods — the **endpoints**:

```bash
kubectl get pods -n taskboard                 # all fine — suspicious
kubectl get endpoints api -n taskboard
```

```
NAME   ENDPOINTS   AGE
api    <none>      2m
```

`<none>` is the smoking gun: the Service currently selects **zero pods**.

```bash
kubectl describe svc api -n taskboard         # Selector: app=apii
kubectl get pods -n taskboard --show-labels   # pods carry app=api
```

**Root cause:** Service selector says `app: apii`, pods are labeled `app: api`.
A Service is only a label query — no matching labels, no endpoints, no traffic.

**Fix:**

```bash
kubectl apply -f k8s/06-api-service.yaml
kubectl get endpoints api -n taskboard   # now lists the pod IPs
```

**Lesson:** Services and pods are connected by nothing but labels.
"Everything Running but no traffic" → check `kubectl get endpoints` first.
