# Build spec — isometric abstraction stack

> **Status: built.** `04-abstraction-layers.png` was generated from
> `04-abstraction-layers.fossflow.json` (FossFLOW/Isoflow format). To edit:
> run FossFLOW locally (`orb start && docker start fossflow`, then
> http://localhost:3400), click the ☰ menu → Open, and select the .json —
> then re-export/screenshot over the PNG. The spec below describes the
> diagram's content.

Five isometric floors stacked bottom-to-top, exploded vertically. Each floor
carries small 3D blocks for the components that layer brings. Color ramp:
gray floor at the bottom, deepening blues going up.

When exported, save the PNG over `docs/diagrams/04-abstraction-layers.png` —
the Helm exercise doc already embeds that path.

## Floor 1 (bottom) — Containers (Docker) — light gray

Blocks on the floor:
- `taskboard-gateway` (nginx image)
- `taskboard-api` (FastAPI image)
- `postgres:16` (official image)
- `taskboard-net` (network — flat pad the three images sit near)
- `taskboard-data` (volume — small cylinder next to postgres)

Edge caption: *adds packaging + isolation · keeps your app code · hides
"works on my machine"*

## Floor 2 — Kubernetes — pale blue

Blocks:
- Pods: `gateway`, `api ×2`, `postgres` (same three apps from Floor 1,
  now duplicated/managed — visually echo the Floor 1 blocks)
- `Service: gateway (NodePort)`, `Service: api`, `Service: db` (flat pads in
  front of their pods)
- `PVC: postgres-data` (cylinder under the postgres pod)
- `Secret` + `ConfigMap ×2` (small flat tiles at the floor's edge)

Edge caption: *adds scheduling, self-healing, scaling, DNS · keeps the same
images · hides manual run/stop/wire*

## Floor 3 — Helm — mid blue

Blocks (fewer, bigger — the floor consolidates):
- `Chart: taskboard` (one large box "containing" miniatures of Floor 2's objects)
- `values.yaml` (document tile leaning on the chart)
- `Release` (tag/label block)
- `helm` CLI (small terminal block)

Edge caption: *adds one installable package + release lifecycle · keeps the
same K8s objects · hides per-environment YAML editing*

## Floor 4 — EKS (managed Kubernetes) — deeper blue

Blocks:
- `Managed control plane` (locked/branded box — visually distinct, AWS-run)
- `Node group` (row of 3 identical node blocks with autoscaling arrow)
- `IAM` · `Load Balancer` · `EBS StorageClass` (three small cloud-service tiles)

Edge caption: *adds managed control plane + cloud wiring · keeps the same
kubectl/manifests/charts · hides etcd and cluster upgrades*

## Floor 5 (top) — Rafay — deepest blue

Blocks:
- `Console` (one central control-point block)
- `Blueprint` + `Policy` (stacked tiles)
- `GitOps pipeline` (conveyor/arrow block feeding downward)
- Mini cluster tokens ×3 (small copies of Floor 4, showing "many clusters")

Edge caption: *adds fleet-wide control — blueprints, policy, GitOps · keeps
clusters and workloads as-is · hides per-cluster one-at-a-time ops*

## Cross-floor thread (the key visual)

One vertical dotted line rising through all floors, following the api app:
`taskboard-api image → api pods → inside the chart → running on a node →
managed in the fleet`. It shows nothing is replaced — each floor wraps the
one below.

## Labels

- Floor name on the front-left edge of each platform, bold.
- Per-floor ADDS/KEEPS/HIDES caption in small text along the front edge
  (or as the floor's tooltip/note if the tool supports it).
