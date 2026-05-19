# MAST Evaluation Methodology

Mobile Application Security Testing combines static analysis of the
binary with dynamic analysis on a device / emulator. Tools differ in
the binaries they accept (APK / AAB / IPA), what they reverse, and
how their dynamic component handles instrumentation.

## Criteria

| Criterion | What to measure | How |
| --- | --- | --- |
| Binary support | Android APK, AAB; iOS IPA; Mach-O binaries | Try each |
| Static analysis depth | Manifest, hardcoded secrets, insecure storage, weak crypto, exported components | Inspect findings against MASVS |
| Native code analysis | C/C++ / Swift / Kotlin Native binaries | Try if relevant |
| Dynamic analysis | Emulator / real device; rooted / jailbroken or unrooted | Confirm options |
| Instrumentation | Frida / Objection integration; hooking support | Try |
| Network capture | TLS pinning bypass; CA installation; HTTP intercept | Try on a pinned app |
| MASVS alignment | Findings tagged to MASVS-AUTH / MASVS-STORAGE / etc. | Inspect |
| MASTG coverage | Which MASTG techniques the tool executes | Inspect |
| OWASP / CWE tagging | Each finding mapped | Inspect |
| Reporting | Severity, evidence, repro steps, screenshots | Inspect |
| CI integration | Build pipeline integration; per-PR or per-release | Hands-on |
| Multi-platform scan in one tool | Android AND iOS from one tool? | Confirm |
| SBOM / dependency scan | Library dependencies of the mobile app | Inspect |
| Operational deployment | SaaS, self-host, on-premises | Confirm |

## Test corpus

- A representative APK and IPA from your team (or production builds
  for staging).
- DIVA / AndroGoat / OWASP MASTG samples for known-vuln Android.
- iGoat / DVIA for iOS.
- A real (non-vuln) build for false-positive baselining.

## Static-side checklist

- Manifest review:
  - `android:allowBackup` set correctly.
  - `android:debuggable` is false in release.
  - Exported components have intent filters and not-arbitrary
    permission requirements.
  - URL schemes / app links verified.
- Secrets scan in the binary (gitleaks-style + Mach-O / DEX-specific
  patterns).
- Crypto choices in the binary (MD5, weak random, hardcoded keys,
  custom crypto).
- Insecure storage (SharedPreferences without encryption,
  unencrypted SQLite, Keychain accessibility levels on iOS).
- TLS configuration: network security config (Android) and ATS
  exceptions (iOS).
- Code obfuscation / anti-tamper presence (informational).

## Dynamic-side checklist

- TLS pinning bypass for testing (requires rooted / jailbroken device
  or runtime instrumentation).
- Insecure data at rest after typical user flows.
- Logging / pasteboard exposure.
- Deep-link / intent-filter exploitation.
- IPC misuse: exported content providers, Android Intents, iOS
  URL schemes / Universal Links, App Groups.

## Scoring matrix

| Criterion | Weight | Tool A | Tool B |
| --- | --- | --- | --- |
| MASVS alignment of findings | 20% | 5 | 3 |
| Dynamic instrumentation quality | 15% | 4 | 5 |
| TLS pinning bypass support | 15% | 5 | 4 |
| iOS + Android in one tool | 10% | 5 | 4 |
| MASTG coverage | 10% | 4 | 3 |
| CI integration | 10% | 3 | 5 |
| Reporting / evidence | 10% | 4 | 4 |
| Operational deployment | 5% | 3 | 5 |
| Pricing | 5% | 3 | 4 |
| Weighted total | -- | 4.2 | 4.0 |

## Common pitfalls

- Comparing on `apkx` / `objection` output rather than the full
  product. Open-source primitives are often more capable per task;
  the commercial product's value is integration and reporting.
- Skipping iOS where the team ships both platforms. iOS tooling
  has different gaps than Android; a tool good at one may be poor
  at the other.
- Ignoring real-device vs emulator behaviour. Some bugs (Secure
  Enclave, biometric prompts, App Attest) only reproduce on real
  devices.
- Treating the static report as sufficient. Dynamic analysis catches
  TLS bypasses, authentication flows, and runtime checks that static
  tooling cannot.

## References

- OWASP MASVS: <https://mas.owasp.org/MASVS/>
- OWASP MASTG: <https://mas.owasp.org/MASTG/>
- MobSF (open-source MAST): <https://mobsf.github.io/docs/>
- Frida: <https://frida.re/docs/>
- Objection: <https://github.com/sensepost/objection>
- Android security best practices: <https://developer.android.com/topic/security/best-practices>
- Apple Platform Security: <https://support.apple.com/guide/security/welcome/web>
- OWASP Mobile Security Testing Guide checklists (per MASVS chapter): <https://mas.owasp.org/checklists/>
