# Concurrency Pitfalls

## Threat

Go's goroutines make concurrency cheap; the bugs that follow are
expensive. Data races corrupt state in undetectable ways; TOCTOU lets
an attacker race the gap between a check and a use; goroutine leaks
DoS the process; closing shared channels causes panics that can be
attacker-triggered.

CWE: CWE-362 (Concurrent Execution using Shared Resource with Improper
Synchronization), CWE-367 (TOCTOU), CWE-401 (Missing Release of Memory
after Effective Lifetime), CWE-833 (Deadlock).

## Insecure

```go
// Unsynchronized map — concurrent writes panic at runtime.
var cache = map[string]string{}
go func() { cache["k"] = "v" }()
go func() { _ = cache["k"] }()

// TOCTOU on a file.
if _, err := os.Stat(path); err == nil {
    f, _ := os.Open(path)                       // raced and replaced by symlink
    // ...
}

// Goroutine leak — never reads from c on the error path.
func work(ctx context.Context) {
    c := make(chan result)
    go func() { c <- doWork() }()
    select {
    case r := <-c:
        handle(r)
    case <-ctx.Done():
        return                                  // sender goroutine blocks forever
    }
}
```

## Why it fails

- Concurrent map access is detected by the runtime in some cases and
  panics; in other cases the map is silently corrupted.
- `os.Stat` then `os.Open` is two syscalls; the filesystem entry can
  change between them. With symlink-following operations, an attacker
  who can write within the same directory may swap the target.
- A goroutine that publishes to an unbuffered channel blocks until a
  receiver reads. If the receiver returns early, the sender lingers
  forever, holding its closure and connection resources.

## Secure

```go
// Use sync primitives or sync.Map for shared maps.
import "sync"
type cache struct {
    mu sync.RWMutex
    m  map[string]string
}
func (c *cache) Get(k string) (string, bool) {
    c.mu.RLock()
    defer c.mu.RUnlock()
    v, ok := c.m[k]
    return v, ok
}

// For file operations, open by handle and act on the handle, not by re-opening by path.
f, err := os.OpenFile(path, os.O_RDONLY|os.O_NOFOLLOW, 0)
if err != nil { return err }
defer f.Close()
info, err := f.Stat()                            // operates on the open handle
// ...

// Goroutine that respects context for cleanup.
func work(ctx context.Context) error {
    c := make(chan result, 1)                    // buffered so sender can exit
    go func() {
        c <- doWork(ctx)                         // doWork honours ctx
    }()
    select {
    case r := <-c:
        return handle(r)
    case <-ctx.Done():
        return ctx.Err()
    }
}
```

Run the race detector in tests and at least one CI lane:

```text
go test -race ./...
go build -race ./cmd/server                      # never ship -race in prod
```

## Notes

- `sync.Mutex` zero value is usable; copy a struct that embeds a mutex
  and you copy lock state. Use a pointer to the struct.
- `sync.Map` is tuned for "write once, read many" or "key disjoint"
  workloads; for mixed read/write, a plain map with `sync.RWMutex` is
  often faster.
- Avoid closing a channel from multiple goroutines; either the sender
  closes or a single coordinator does.
- For long-running services, use `errgroup.WithContext` to cancel
  sibling goroutines when one fails.
- TOCTOU also bites command execution: validating the file at path,
  then passing the path to a subprocess, re-resolves the path. Use the
  open file descriptor (`/proc/self/fd/<n>` on Linux) where the
  primitive supports it.

## References

- Go Memory Model: <https://go.dev/ref/mem>
- Go `sync` package: <https://pkg.go.dev/sync>
- Go race detector: <https://go.dev/doc/articles/race_detector>
- CWE-362: <https://cwe.mitre.org/data/definitions/362.html>
- CWE-367: <https://cwe.mitre.org/data/definitions/367.html>
