# Interview cheat sheet (generated)

Generated with `physis cheat --track <track> --commands --budget 2000` over the committed corpus in this directory,
reproducible from the corpus fingerprint printed in each block.

One line per primitive: `id — invariant | $ first command`. Deep material (2-minute answers, examples, sources,
failure modes, misuse signatures) is deliberately **not** here — it is loaded on demand with
`physis prim <id> --depth deep` or `:explain` in the HUD.

## Kubernetes

```
CHEATSHEET kubernetes (45 lines · corpus 2c855769 · budget 2000 · commands)
  k8s.api-server — The API server is the single front door: it authenticates, authorizes, validates and persists objects, and every other component talks only to it. | $ kubectl auth can-i create deployments -n payments
  k8s.service.clusterip — A virtual IP reachable only from inside the cluster, load-balanced across ready endpoints. | $ kubectl get svc api -o yaml
  k8s.configmap — Non-secret configuration is stored as a namespaced object and mounted or injected as env. | $ kubectl get configmap -A
  k8s.controller — A controller is a reconciliation loop over a resource type; an operator is a controller that packages domain operational knowledge for one application. | $ kubectl get events --field-selector involvedObject.kind=MyResource
  k8s.cron-job — A CronJob creates a Job on a cron schedule, with an explicit concurrency and history policy. | $ kubectl get cronjobs -A
  k8s.daemon-set — Exactly one Pod per eligible node, including nodes added later. | $ kubectl get daemonset -A
  k8s.debugging-workflow — Always separate the four layers in order: object state, events, container logs, then network path. | $ kubectl get pods -o wide
  k8s.deployment — The replica count is declared; the Deployment controller converges Pods to it via ReplicaSets. | $ kubectl get deployments -A
  k8s.describe — describe renders the spec, the observed status and the recent events of one object in one place. | $ kubectl describe pod api-...
  k8s.desired-state — You submit the desired state; controllers compare it with observed state and act on the difference.
  k8s.dns-service-discovery — Every Service gets a DNS name `<service>.<namespace>.svc.cluster.local` resolving to its ClusterIP. | $ kubectl get svc -n kube-system
  k8s.endpoints — The endpoint list is the actual set of Pod IPs traffic is sent to, derived from the selector plus readiness. | $ kubectl get endpoints api
  k8s.etcd — etcd is the only stateful store; it holds every object and is a quorum-replicated log, so writes need a majority and the cluster needs a working quorum. | $ kubectl get pods -n kube-system
  k8s.events — Events are short-lived records of what controllers did and why, including scheduling and probe failures. | $ kubectl get events --sort-by=.metadata.creationTimestamp
  k8s.exec — exec starts a process in an existing container namespace, so it sees the container's network and filesystem but changes nothing about the image. | $ kubectl exec -it api-7d9f-abc -- sh
  k8s.headless-service — With clusterIP None there is no virtual IP and no load balancing; DNS returns the Pod IPs directly.
  k8s.hpa — The HPA adjusts replica count toward a target metric ratio, bounded by min/max and by cooldowns. | $ kubectl get hpa
  k8s.ingress — Ingress is L7 routing rules evaluated by an ingress controller that terminates the connection. | $ kubectl get ingress -A
  k8s.job — A Job runs Pods until a declared number of successful completions is reached. | $ kubectl get jobs -A
  k8s.kubelet — The kubelet is the per-node agent that runs the PodSpecs assigned to its node and reports their status back. | $ kubectl describe node <node>
  k8s.labels-selectors — Controllers, Services and policy select objects by label equality or set expressions, never by name. | $ kubectl get pods -l app=api,version=v2
  k8s.service.loadbalancer — The cloud controller provisions one external load balancer per Service of this type. | $ kubectl get svc -o wide
  k8s.logs — Container stdout/stderr is captured per container and is lost when the container is deleted unless shipped elsewhere. | $ kubectl logs api-7d9f-abc
  k8s.namespace — A namespace scopes names, RBAC, quotas and most policy objects; it is not a network or kernel boundary. | $ kubectl get ns
  k8s.node — A node is a machine (or VM) with a kubelet, a container runtime and allocatable capacity that the scheduler fills with Pods. | $ kubectl get nodes -o wide
  k8s.service.nodeport — The service is reachable on a static port on every node IP, in addition to its ClusterIP.
  k8s.pod — A Pod is one scheduling unit; containers in it share network and can share volumes.
  k8s.port-forward — port-forward opens a tunnel through the API server to one Pod (or one Service), bypassing Services and Ingress. | $ kubectl port-forward svc/api 8080:80
  k8s.probe.liveness — A failing liveness probe restarts the container; it answers "is this process wedged", never "is a dependency down". | $ kubectl get pods
  k8s.probe.readiness — A Pod receives Service traffic only while its readiness probe passes; failure removes it from the endpoint list without restarting it. | $ kubectl get pods -o wide
  k8s.probe.startup — A startup probe suspends liveness and readiness checks until the process has finished booting.
  k8s.pvc — A PVC is a request for storage that binds to a PersistentVolume (statically or dynamically) and survives Pod rescheduling. | $ kubectl get pvc -A
  k8s.reconciliation — A loop that reads desired state, reads observed state, computes a diff and acts, then repeats -- never a one-shot command sequence. | $ kubectl get <kind> -o yaml
  k8s.replica-set — A ReplicaSet maintains a set of identical Pods matching a selector. | $ kubectl get rs -o wide
  k8s.resources.limits — Limits are enforcement: exceeding a memory limit kills the container, exceeding a CPU limit throttles it. | $ kubectl top pod
  k8s.resources.requests — Requests are what the scheduler reserves for placement and what QoS is computed from. | $ kubectl describe node <node>
  k8s.rollback — Revision history holds previous Pod templates, so a rollback is a template change the Deployment controller applies again. | $ kubectl rollout history deployment/api
  k8s.deployment.rolling-update — Maintain enough healthy replicas while replacing the old ReplicaSet. | $ kubectl rollout status deployment/api
  k8s.scheduler — The scheduler assigns a node to each unbound Pod by filtering feasible nodes (resources, taints, affinity) and scoring the rest; it never starts containers. | $ kubectl describe pod api-...
  k8s.secret — Secrets are configuration objects with special handling (not encryption by default) intended for sensitive values. | $ kubectl get secret -A
  k8s.service — A Service is a stable virtual IP and DNS name that load-balances to the Pods currently matching its selector. | $ kubectl get svc -A
  k8s.stateful-set — Each replica keeps a stable ordinal identity and its own PersistentVolumeClaim across restarts. | $ kubectl get statefulset -o wide
  k8s.storage-class — A StorageClass names a provisioner plus parameters, so PVCs are satisfied without pre-created volumes. | $ kubectl get storageclass
  k8s.top-resource-usage — `kubectl top` reports live usage from the metrics pipeline, which is separate from the scheduler's view of requests. | $ kubectl top pod -A
  k8s.volume — Container filesystems are ephemeral; anything that must outlive a container restart lives in a Volume.
  [45/45 lines · 1593 tokens of 2000 budget] · deep detail: :prim <id> --depth deep

```

## Rust

```
CHEATSHEET rust (38 lines · corpus 2c855769 · budget 2000 · commands)
  rust.anyhow-thiserror — thiserror for typed, matchable errors at boundaries -- including the status code at an HTTP boundary; anyhow for context-rich, opaque errors inside an application.
  rust.app-state — One state value is built at startup, wrapped in Arc and cloned cheaply into every handler and task.
  rust.arc — Arc shares immutable ownership by atomic reference counting; it is alive until the last handle drops.
  rust.async-streams — A Stream yields items over time, pulled by the consumer, so backpressure comes from the consumer not asking for the next item.
  rust.atomics — An atomic update is indivisible and ordered by a memory ordering you must choose.
  rust.axum — A handler is an async function whose arguments are typed extractors, and the router turns it into a Tower service.
  rust.blocking-in-async — A blocking call on a runtime worker stalls every task scheduled on that thread, so blocking work belongs in spawn_blocking or a dedicated pool.
  rust.borrow-lifetimes — A lifetime names how long a borrow must stay valid; it constrains relationships, it never extends a value's life.
  rust.bounded-concurrency — Concurrency is a limit you choose, so memory stays proportional to the limit rather than to the input.
  rust.cancellation — Futures are cancelled by being dropped, so cancellation is cooperative and every await is a cancellation point.
  rust.connection-pool — A pool bounds concurrent database work, so pool size is a backpressure decision rather than a performance dial.
  rust.dyn-vs-generic — dyn gives one code path with runtime dispatch and heterogeneous collections; generics give per-type copies with compile-time dispatch.
  rust.error-enum — Each variant encodes a distinct caller decision, so callers can match instead of parsing messages.
  rust.generics-monomorphization — Generic code is compiled once per concrete type, so dispatch is free at runtime and the cost is binary size plus compile time.
  rust.graceful-shutdown — On shutdown: stop accepting, cancel background work, drain in-flight requests under a deadline, then exit.
  rust.mutex-across-await — A std guard is not Send and blocks the OS thread, so holding it across an await either fails to compile in a spawned task or stalls that worker.
  rust.mutex — A mutex serializes access to the value it guards, so contention on a hot lock serializes unrelated work; which mutex you choose must match whether the critical section may await.
  rust.ownership-move — One owner per value; passing by value moves it, borrowing is a loan the compiler tracks.
  rust.question-mark — `?` early-returns on Err after applying `From` conversion to the enclosing function's error type.
  rust.raii — Destructors run when a value leaves scope, on early return and on panic unwind, so release logic belongs in Drop.
  rust.rc-vs-arc — Rc counts non-atomically so it is neither Send nor Sync; Arc pays an atomic per clone to be shareable.
  rust.result — A Result makes failure a value in the type, so the compiler forces every caller to decide what to do with it.
  rust.retry — Retry only idempotent operations, with exponential backoff plus jitter, a bounded attempt count and a total deadline.
  rust.rwlock — RwLock allows many readers or one writer, so it wins only when reads dominate and the read path is non-trivial.
  rust.send-sync — Send allows moving a value to another thread; Sync allows sharing references from another thread (so &T is Send).
  rust.serde — Derived serde impls are a declarative mapping from the type; attributes decide names, defaults and strictness, so the wire format is explicit.
  rust.timeout — A timeout bounds how long the caller waits; it does not guarantee the underlying work stopped.
  rust.tokio-broadcast — Every subscriber receives every message, and a subscriber that falls behind gets Lagged instead of slowing the producer down.
  rust.tokio-join — join! awaits futures concurrently inside one task and returns every result; it never cancels a branch.
  rust.tokio-mpsc — A bounded mpsc channel moves owned messages from many senders to one receiver, and a full channel makes send().await wait.
  rust.tokio-oneshot — oneshot carries exactly one value from one sender to one receiver; dropping the sender makes the receiver resolve with an error instead of hanging.
  rust.tokio-select — select! completes with one ready branch -- polling order unless you write `biased;` -- and drops the others, so every await inside it is a potential cancellation point.
  rust.tokio-semaphore — A Semaphore issues a fixed number of permits; acquiring one gates entry and dropping the guard releases it.
  rust.tokio-spawn — A spawned task is an independent, 'static, Send future: it keeps running after the caller returns and its result is only reachable through the JoinHandle.
  rust.tokio-watch — watch holds exactly one latest value; receivers observe changes and can always read the current value, so late readers stay correct.
  rust.tower — Middleware is a Tower layer wrapping a Service, so the same policy types apply to inbound and outbound calls.
  rust.tracing — Spans carry context across awaits and tasks; events carry facts with structured fields.
  rust.traits — Traits define behaviour in terms of the implementer; generic bounds monomorphise, dyn Trait dispatches through a vtable.
  [38/38 lines · 1185 tokens of 2000 budget] · deep detail: :prim <id> --depth deep

```

## Architecture (design primitives + recipes)

```
CHEATSHEET architecture (47 lines · corpus 2c855769 · budget 2000 · commands)
  design.backpressure — When producers outrun consumers, the system must push back, drop, or buffer -- an unbounded buffer is not a solution, it is a delayed failure. | $ kubectl top pod
  design.bounded-queue — A queue has a finite capacity and a declared overflow policy, so latency and memory stay bounded under load. | $ kubectl top pod
  design.cache-aside — The application reads the cache, falls back to the source of truth on a miss, and populates the cache with a TTL.
  design.cache-invalidation — Every cache entry has a defined lifetime and a defined invalidation trigger; staleness is bounded by configuration, not by hope.
  design.circuit-breaker — After a threshold of failures the breaker opens, failing calls immediately without touching the dependency, and half-opens periodically to test recovery.
  design.connection-pool — A connection pool is a concurrency limit on a shared resource; its size is bounded by the resource, not by the client's parallelism.
  design.distributed-locking — A distributed lock is a lease with a TTL and a unique holder token; every acquisition, renewal and release must be atomic and owned.
  design.exactly-once — Delivery is at-least-once or at-most-once; "exactly once" is achieved only as at-least-once delivery plus idempotent or deduplicated processing.
  design.file-pipeline — Files are ingested to durable storage first, then processed in bounded, resumable, idempotent stages keyed by a content address.
  design.graceful-shutdown — Stop accepting, finish in-flight work (idempotent or requeueable) within a deadline, then exit -- with clients retrying in the window where the endpoint list and the process disagree.
  design.health-checking — Separate liveness (should this process be restarted) from readiness (should traffic be sent here), and keep both cheap and dependency-aware in the right direction.
  design.idempotency — An idempotent operation has the same effect whether it runs once or many times, which is what makes retries, redelivery and reconciliation safe.
  design.leader-election — Exactly one instance holds leadership at a time, leadership is renewed through a lease, and losing the lease stops the leader's work. | $ kubectl get leases -n kube-system
  design.load-shedding — Under overload, reject or downgrade work early and deliberately so the requests that are served still meet their latency budget.
  design.telemetry-pipeline — High-volume telemetry must be aggregated and batched as early as possible, and losing some samples is acceptable by design.
  design.observability — Metrics answer "how much"; logs answer "what happened once"; traces answer "where the time went". Each has its own cost model.
  design.producer-consumer — A queue between the two sides decouples their rates; the queue depth is then a first-class observable.
  design.rate-limiting — Requests are admitted against a budget per identity and window, with a defined response when the budget is exhausted. | $ kubectl get ingress -A
  design.redis-cache — Redis is an in-memory, single-threaded-per-shard key/value store: excellent for derived, volatile state and coordination, dangerous as a system of record without persistence and a plan. | $ redis-cli --latency
  design.retry-backoff — Retry transient failures only, with exponential delay plus jitter, a bounded attempt count and a deadline shared with the caller.
  design.schema-migration — Every schema change must be compatible with both the old and the new version of the application code while both are running.
  design.semaphore — A semaphore issues a fixed number of permits; acquisition gates entry, release is guaranteed by scope.
  design.service-discovery — Callers resolve a stable name to the current set of healthy instances, so addresses are never hardcoded. | $ kubectl get endpoints <svc>
  design.shared-state — Shared mutable state is a design choice with a cost model; the alternatives are ownership transfer, immutable snapshots and single-owner serialization.
  design.state-machine — Enumerate states and legal transitions, store the current state, and make every transition idempotent.
  design.timeouts — Every network call has a deadline derived from the caller's remaining budget, and deadlines shrink as they propagate down the stack.
  design.worker-pool — A fixed set of consumers pulls from a shared bounded queue, so concurrency is a number you chose and can reason about.
  recipe.async-job-processing — Accept fast, persist durably, process with bounded concurrency, and make every job idempotent so redelivery is free.
  recipe.cache-backed-api — The database stays the source of truth; the cache is derived, bounded by TTL and invalidated on write.
  recipe.controller — Observe current state, diff against desired state, act on the difference, record status, repeat -- never a one-shot script.
  recipe.database-backed-api — The database is the source of truth and a shared, finite resource; every path to it goes through a bounded pool with explicit transaction scope.
  recipe.distributed-worker-pool — Ownership is held through a visibility timeout or lease, so concurrency is bounded per item while replicas scale freely.
  recipe.event-ingestion — Persist before acknowledging, partition by key for ordering, and bound every hop so that backpressure reaches the producer.
  recipe.file-processing-pipeline — Store the bytes durably, queue only references, process in bounded idempotent stages keyed by content digest.
  recipe.graceful-shutdown — Shutdown is an ordered protocol: stop admitting, stop pulling, finish or requeue what is in flight, then exit inside the grace period.
  recipe.high-throughput-telemetry — Aggregate early, batch always, bound every buffer, and accept deliberate loss -- telemetry must never be able to block the applications it observes.
  recipe.incident-diagnosis — Establish scope, read the declared-versus-observed state, reconstruct the timeline, and only then act -- restarts destroy evidence.
  recipe.local-to-kubernetes — One image, many environments: build the same artifact, inject all configuration, and make the local loop fast enough to run the checks that only the cluster can fail.
  recipe.rate-limited-api — Every request is admitted against a per-identity budget, and the rejection is explicit (429 with Retry-After), so clients can behave correctly.
  recipe.redis-backed-service — Redis stores derived, reconstructible state (cache, counters, sessions, locks), never the only copy of data you cannot rebuild.
  recipe.resilient-dependent-service — Treat the dependency as a failure source by default: bound every call, retry only idempotent operations with jitter, break the circuit, and have a degraded path that does not need it.
  recipe.rest-api — Each request is independent; all state lives in a database or cache, so replicas are interchangeable.
  recipe.service-debugging — Work from the outside in and from the aggregate to the specific: symptoms first, then the layer that owns them, then the single request that demonstrates it.
  recipe.service-discovery — Callers use stable names that resolve to the current healthy set, so scaling and replacement are invisible to them.
  recipe.stateful-workload — Identity and storage must be stable across restarts, and quorum must be respected when replicas come and go.
  recipe.webhook-receiver — Acknowledge within the sender's timeout, verify authenticity before acting, and process asynchronously with deduplication -- senders retry, so delivery is at-least-once.
  recipe.zero-downtime-deploy — Keep serving while the version changes: overlap capacity, gate traffic on readiness, drain on termination, and keep old and new versions compatible during the window.
  [47/47 lines · 1695 tokens of 2000 budget] · deep detail: :prim <id> --depth deep

```
