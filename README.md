<div align="center">
  <img src="./assets/banner.png" alt="AppSec Handbook">
</div>

# AppSec Handbook

A working reference for application security and secure SDLC: secure coding,
threat modeling, DevSecOps pipelines, framework mappings, architecture patterns,
tooling evaluation methodology, and finding writeups.

This repository focuses on the defensive side of AppSec. Offensive cheatsheets,
payloads, and pentest tooling live in a separate repository:
<https://github.com/maverick-hackz/Workstation>

## Contents

| Section | Purpose |
| --- | --- |
| [Secure coding](secure-coding/) | Language-specific guidelines with insecure to secure examples |
| [Threat modeling](threat-modeling/) | STRIDE/PASTA/Attack Trees methodology, templates, worked examples |
| [Secure SDLC](secure-sdlc/) | Requirements, code review, security gates, VDP templates |
| [DevSecOps](devsecops/) | CI/CD security templates, pre-commit, custom Semgrep rules, K8s policies |
| [Frameworks](frameworks/) | ASVS, SAMM, NIST SSDF, OWASP Top 10 (Web/API/LLM/CI-CD), CWE Top 25 |
| [Architecture](architecture/) | Zero Trust, OAuth2/OIDC/SAML/mTLS, crypto, secrets management |
| [Tooling evaluation](tooling-evaluation/) | SAST/SCA/DAST/MAST/ASPM evaluation methodology |
| [Writeups](writeups/) | Sanitized finding writeups: Finding -> Impact (CVSS 3.1) -> Repro -> Fix |
| [References](references/) | Reading list, standards, conferences, glossary |

## Intended audience

- AppSec engineers building or reviewing secure SDLC programs
- Developers integrating security into CI/CD
- Security architects working on auth, crypto, API security
- Hiring managers evaluating AppSec engineering depth

## See also

- Offensive cheatsheets and pentest tooling: [Workstation](https://github.com/maverick-hackz/Workstation)

## License

[MIT](LICENSE)
