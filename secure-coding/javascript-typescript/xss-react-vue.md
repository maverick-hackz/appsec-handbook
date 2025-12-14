# XSS in React and Vue

## Threat

React and Vue both auto-escape interpolated values in templates / JSX.
The escape hatches (`dangerouslySetInnerHTML`, `v-html`,
`document.write`, direct DOM manipulation, `eval`-using libraries) bypass
auto-escape. URL contexts (`href`, `src`) require additional validation;
auto-escape does not stop `javascript:` URIs.

CWE: CWE-79 (XSS), CWE-80 (Improper Neutralization of Script-Related
HTML Tags in a Web Page), CWE-87 (Improper Neutralization of Alternate
XSS Syntax).

## Insecure (React)

```jsx
function Comment({ html }) {
    return <div dangerouslySetInnerHTML={{ __html: html }} />;
}

function Link({ url }) {
    return <a href={url}>open</a>;                  // javascript:... slips through
}
```

## Insecure (Vue 3)

```vue
<template>
  <div v-html="comment"></div>                       <!-- v-html bypasses escape -->
  <a :href="url">open</a>                            <!-- same javascript: risk -->
</template>
```

## Why it fails

- Auto-escape is for HTML body and attribute text. URL parsing requires
  a scheme allowlist; `javascript:`, `data:text/html`, and `vbscript:`
  execute in the navigation context.
- `dangerouslySetInnerHTML` and `v-html` pass the raw string to
  `innerHTML`; the browser parses it as HTML.

## Secure

Render untrusted data with normal interpolation:

```jsx
<div>{comment}</div>                                 // React auto-escapes
```

```vue
<div>{{ comment }}</div>                             <!-- Vue auto-escapes -->
```

Allow rich text by sanitizing first:

```jsx
import DOMPurify from "dompurify";

function Comment({ html }) {
    const clean = DOMPurify.sanitize(html, {
        ALLOWED_TAGS: ["b", "i", "em", "strong", "a", "p", "br", "ul", "ol", "li"],
        ALLOWED_ATTR: ["href"],
    });
    return <div dangerouslySetInnerHTML={{ __html: clean }} />;
}
```

URL allowlist:

```javascript
function safeUrl(input) {
    try {
        const u = new URL(input, window.location.origin);
        if (u.protocol !== "https:" && u.protocol !== "http:" && u.protocol !== "mailto:") {
            return "#";
        }
        return u.toString();
    } catch {
        return "#";
    }
}

<a href={safeUrl(url)}>open</a>
```

Pin a Content-Security-Policy that forbids inline scripts unless
nonce-allowlisted:

```text
Content-Security-Policy:
  default-src 'self';
  script-src 'self' 'nonce-<per-request-nonce>';
  object-src 'none';
  base-uri 'self'
```

## Notes

- React still renders the value of `style={...}` from an object; do not
  build the object from untrusted strings (`backgroundImage`).
- `target="_blank"` links should pair with `rel="noopener noreferrer"`
  to prevent reverse tabnabbing and Referer leakage. React 17+ adds
  `rel="noopener noreferrer"` automatically; verify the toolchain still
  does so.
- Server-side rendering (Next.js, Nuxt) does not change escape behaviour
  for interpolated values, but does evaluate `dangerouslySetInnerHTML`
  at SSR time — the same rules apply.
- Markdown-to-HTML libraries differ: `marked` is safe-by-default in
  recent versions; older versions and naive `markdown-it` plugins
  pass through raw HTML. Always sanitize the rendered HTML with
  `DOMPurify` (browser) or `isomorphic-dompurify` (SSR).

## References

- OWASP XSS Prevention Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html>
- OWASP DOM-based XSS Prevention Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html>
- React `dangerouslySetInnerHTML`: <https://react.dev/reference/react-dom/components/common>
- Vue 3 — Security: <https://vuejs.org/guide/best-practices/security.html>
- DOMPurify: <https://github.com/cure53/DOMPurify>
- MDN — Content Security Policy: <https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP>
