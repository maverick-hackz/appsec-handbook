# Path Traversal

## Threat

User input flows into `os.Open` / `os.ReadFile` / `http.ServeFile` /
`filepath.Join` without an anchor to a base directory. `..` segments,
absolute paths, or symlinks expose arbitrary files.

CWE: CWE-22 (Improper Limitation of a Pathname to a Restricted Directory),
CWE-23 (Relative Path Traversal), CWE-59 (Improper Link Resolution).

## Insecure

```go
// Trust user input directly
file := req.URL.Query().Get("file")
data, err := os.ReadFile(file)             // "/etc/passwd" wins

// Join doesn't anchor
data, err := os.ReadFile(filepath.Join("/var/www/uploads", file))
// file = "../../etc/passwd" -> "/etc/passwd"

// http.ServeFile with user-controlled path
http.ServeFile(w, r, filepath.Join("uploads", r.URL.Path))
```

## Why it fails

- `filepath.Clean` collapses `..` but resolves the result relative to
  the current root, not to the intended base. The cleaned path can
  still escape if the base is concatenated naively.
- A symlink inside the base directory can point at a file outside; an
  attacker who can plant files (uploads, sync) can chain that.
- `http.ServeFile` historically protected against `..` in the URL path
  but not against constructed paths where the developer did the join.

## Secure

Go 1.24 introduced `os.Root` for filesystem operations anchored to a
specific directory:

```go
// Go 1.24+
root, err := os.OpenRoot("/var/www/uploads")
if err != nil { return err }
defer root.Close()

f, err := root.Open(userPath)              // refuses paths that escape
if err != nil { return err }
defer f.Close()
```
<!-- TODO: verify os.OpenRoot semantics and edge cases against Go release notes -->

Pre-1.24 / general:

```go
const base = "/var/www/uploads"

cleaned := filepath.Clean("/" + userPath)               // collapse to absolute-ish
joined  := filepath.Join(base, cleaned)
abs, err := filepath.Abs(joined)
if err != nil { return err }

baseAbs, err := filepath.Abs(base)
if err != nil { return err }

// Reject paths that escape the base after resolution.
rel, err := filepath.Rel(baseAbs, abs)
if err != nil || strings.HasPrefix(rel, "..") || strings.Contains(rel, ".."+string(filepath.Separator)) {
    return errors.New("invalid path")
}

// Reject symlinks if the application does not need them.
fi, err := os.Lstat(abs)
if err != nil { return err }
if fi.Mode()&os.ModeSymlink != 0 {
    return errors.New("symlinks not allowed")
}

data, err := os.ReadFile(abs)
```

For HTTP serving, prefer `http.FileServerFS` over hand-assembled paths:

```go
fsys := os.DirFS("/var/www/uploads")
http.Handle("/files/", http.StripPrefix("/files/", http.FileServerFS(fsys)))
```

## Notes

- Always validate AND anchor. Validation rejects obvious junk; anchoring
  enforces the result.
- Reject paths that contain NUL bytes (`\x00`), Windows-style separators
  on Linux services if not expected, or paths >= `MAX_PATH`.
- For file uploads, generate the on-disk name server-side (UUID); never
  store the original filename as the path component.

## References

- OWASP Path Traversal: <https://owasp.org/www-community/attacks/Path_Traversal>
- CWE-22: <https://cwe.mitre.org/data/definitions/22.html>
- Go `path/filepath` package: <https://pkg.go.dev/path/filepath>
- Go `os.Root` (Go 1.24): <https://pkg.go.dev/os#Root>
