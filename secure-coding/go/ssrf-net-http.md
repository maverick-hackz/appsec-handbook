# SSRF Prevention in `net/http`

## Threat

An outbound HTTP request to a user-supplied URL targets internal
infrastructure: cloud metadata endpoints (`169.254.169.254`), internal
admin panels, kube-apiserver, link-local, loopback, RFC 1918 networks,
or IPv6 ULA / link-local. Redirects, DNS rebinding, and IPv6 forms
extend the bypass surface.

CWE: CWE-918 (Server-Side Request Forgery). OWASP API Top 10: API7:2023.

## Insecure

```go
url := req.URL.Query().Get("url")          // attacker-controlled
resp, err := http.Get(url)                 // straight to anywhere
defer resp.Body.Close()
```

## Why it fails

- `http.Get` follows redirects by default. An attacker hosts a redirect
  to `http://169.254.169.254/latest/meta-data/iam/security-credentials/`.
- DNS for an attacker-owned host returns a public address for the
  validation request and a private address (or `127.0.0.1`) for the
  fetch (DNS rebinding).
- IPv6, IPv4-mapped IPv6 (`::ffff:127.0.0.1`), and decimal/octal IP
  forms slip past naive checks on a `string`.

## Secure

```go
import (
    "context"
    "errors"
    "fmt"
    "net"
    "net/http"
    "net/url"
    "syscall"
    "time"
)

func isAllowedAddr(addr string) error {
    host, _, err := net.SplitHostPort(addr)
    if err != nil { return err }
    ip := net.ParseIP(host)
    if ip == nil { return fmt.Errorf("unresolved: %s", host) }
    if ip.IsLoopback() || ip.IsPrivate() ||
        ip.IsLinkLocalUnicast() || ip.IsLinkLocalMulticast() ||
        ip.IsUnspecified() || ip.IsMulticast() {
        return fmt.Errorf("blocked range: %s", ip)
    }
    // Cloud metadata service (extra belt and braces).
    if ip.Equal(net.ParseIP("169.254.169.254")) ||
        ip.Equal(net.ParseIP("fd00:ec2::254")) {
        return errors.New("metadata service")
    }
    return nil
}

// Custom dialer that re-validates the resolved address.
dialer := &net.Dialer{Timeout: 5 * time.Second}

control := func(network, address string, c syscall.RawConn) error {
    return isAllowedAddr(address)
}

transport := &http.Transport{
    DialContext: func(ctx context.Context, network, addr string) (net.Conn, error) {
        return (&net.Dialer{
            Timeout: 5 * time.Second,
            Control: control,
        }).DialContext(ctx, network, addr)
    },
    ResponseHeaderTimeout: 5 * time.Second,
    DisableKeepAlives:     true,
}

client := &http.Client{
    Transport: transport,
    Timeout:   10 * time.Second,
    // Refuse redirects so we cannot be bounced into a private range.
    CheckRedirect: func(req *http.Request, via []*http.Request) error {
        return http.ErrUseLastResponse
    },
}

func fetch(rawURL string) (*http.Response, error) {
    u, err := url.Parse(rawURL)
    if err != nil { return nil, err }
    if u.Scheme != "https" && u.Scheme != "http" {
        return nil, errors.New("scheme not allowed")
    }
    return client.Get(u.String())
}
```

Stronger postures:

- Restrict outbound traffic at the network layer (egress policy in the
  VPC / namespace). Defence-in-depth with the application-layer check.
- Use an HTTP proxy that enforces the egress allowlist; the application
  cannot bypass the proxy.

## Notes

- `net.IP.IsPrivate` (Go 1.17+) covers RFC 1918 / RFC 4193, but NOT
  `127.0.0.0/8`, `169.254.0.0/16`, multicast, broadcast — combine with
  the other `Is*` methods as shown.
- IPv6: a literal `[::1]` in a URL parses as loopback; rebinding to
  IPv6 ULA (`fc00::/7`) or to IPv4-mapped IPv6 should be blocked.
- Connection re-use (keepalive) can mask DNS rebinding; either disable
  keep-alives for user-driven fetches or pin the resolved IP for the
  lifetime of the request.
- Audit URL parsing for the user-controlled side: `url.Parse` accepts
  many things (`http://a.com#@b.com`, `http://a.com\@b.com`) that some
  downstream parsers interpret differently.

## References

- OWASP SSRF Prevention Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html>
- CWE-918: <https://cwe.mitre.org/data/definitions/918.html>
- Go `net/http` package: <https://pkg.go.dev/net/http>
- Go `net.IP` reserved-range helpers: <https://pkg.go.dev/net#IP.IsPrivate>
- AWS IMDSv2 (mitigation upstream): <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html>
