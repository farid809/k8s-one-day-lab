# Scenario 4 — Solution

**Symptom:** the claim sits in `Pending` forever:

```bash
kubectl get pvc -n taskboard
NAME           STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS
postgres-data  Bound     pvc-…    1Gi        RWO            standard
reports-data   Pending                                      fast-ssd
```

(Any pod that mounted it would also sit in `Pending` — `describe pod` would say
"pod has unbound immediate PersistentVolumeClaims".)

**Diagnosis path:**

```bash
kubectl describe pvc reports-data -n taskboard
```

Events:

```
storageclass.storage.k8s.io "fast-ssd" not found
```

```bash
kubectl get storageclass      # minikube has exactly one: standard (default)
```

**Root cause:** the claim requests a StorageClass named `fast-ssd`. A
StorageClass is the *recipe* for provisioning disks, and this cluster doesn't
have that recipe — so nothing can ever satisfy the claim. (This is the classic
"manifest worked on the cloud cluster, fails on minikube" failure: the manifest
is portable, the StorageClass names are per-cluster.)

**Fix:** drop the `storageClassName` line so the cluster default is used —
or simply delete the claim, since nothing needs it:

```bash
kubectl delete pvc reports-data -n taskboard
```

**Lesson:** `Pending` means "the cluster cannot satisfy this request" — and for
storage, `describe pvc` + `kubectl get storageclass` show why. `Pending` on pods
works the same way (insufficient CPU/memory, unbound volumes): describe it,
read the events.
