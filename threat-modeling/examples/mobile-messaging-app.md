# Threat Model: Mobile End-to-End Messaging App

A sanitized model of a generic mobile end-to-end encrypted messaging
client. Not a model of any specific product.

## System overview

A native mobile client (iOS and Android) lets a user exchange E2E
encrypted text, voice messages, attachments, and one-to-one or group
calls with contacts. The service delivers ciphertext only; the
encryption keys live on participant devices. Identity is a phone
number or handle bound to a per-device key pair stored in
hardware-backed storage. Sensitive operations (key change, new
device linking, contact disclosure) require biometric step-up.

## Assets

| Asset | Sensitivity | Owner |
| --- | --- | --- |
| Plaintext message content (on participant devices) | Restricted | User |
| Identity / pre-key signing material (Secure Enclave / StrongBox) | Restricted | User |
| Contact graph and metadata at the service | Restricted | Service |
| Push notification payload (preview text, sender) | Confidential | User |
| Device-linking codes (QR pairing) | Restricted | User |
| Application binary and assets | Public | Service |

## Trust boundaries

1. `TB-1` User (cognitive) -> Device
2. `TB-2` App user-space -> Device OS (Secure Element / Keystore)
3. `TB-3` App -> Internet -> Service API (TLS, certificate pinning)
4. `TB-4` Service -> Push providers (APNs, FCM, with encrypted
   payload)
5. `TB-5` App <-> Other apps on the device (intent / URL scheme /
   share sheet, pasteboard)
6. `TB-6` Participant A's device <-> Participant B's device (E2E
   protocol via the service as a relay)

## DFD (text form)

```text
[User A]                                           [User B]
   |                                                   ^
   | type message                                      |
   v                                                   |
(App A) -- encrypt to B's pre-key bundle              (App B)
   |          |                                        ^
   |          v                                        |
   |    [[Secure Enclave A]]                  [[Secure Enclave B]]
   |
   |  HTTPS, pinned cert, app attestation
   v
============== TB-3 INTERNET ==
   |
   v
(Service API) ---- store ciphertext / deliver --> [push provider]
   |                                                       |
   +-- write metadata --> [[Service Store (ciphertext)]]   |
                                                           v
                                                       (App B)
                                                       receive, decrypt
                                                       with Secure Enclave B
```

## Assumptions

1. The OS is not jailbroken / rooted at the time of execution; the app
   detects but cannot prove this rigorously.
2. The user does not enrol another person's biometric on their device.
3. Certificate pinning prevents man-in-the-middle by any actor other
   than the device's system trust store combined with physical
   coercion.
4. The cryptographic protocol (e.g., Signal Protocol / Double Ratchet)
   is implemented from a vetted library; its primitives are not
   re-rolled in this client.
5. App attestation (Apple App Attest, Google Play Integrity) is
   accepted as evidence the binary is unmodified for non-high-risk
   operations; high-risk operations (new device linking, identity-key
   change) require per-operation user confirmation.

## STRIDE analysis

| # | Element | Threat | STRIDE | Mitigation | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | User | Coerced device unlock (rubber-hose) | S | Optional decoy / hidden profile; on-device per-conversation passcode for sensitive threads | Partial |
| 2 | App | Reverse engineering to extract embedded secrets | I | No long-lived shared secrets in the binary; per-install ephemeral keys generated client-side; obfuscation reduces, does not prevent | Done |
| 3 | App | Tampered app re-published (sideloaded) | T | App attestation enforced server-side; refusal to operate without a valid attestation token; warning shown if attestation lapses | Done |
| 4 | App | Malicious overlay / screen capture | I, T | Anti-screenshot on sensitive screens (Android FLAG_SECURE, iOS view-layer block); accessibility-service blocklists; OS overlay detection | Partial |
| 5 | App | Clipboard exfiltration of message text | I | Sensitive fields marked non-extractable; auto-clear pasteboard with a TTL; per-app pasteboard isolation where supported | Done |
| 6 | Secure Enclave | Key extraction | I | Keys generated and used only inside the Secure Enclave / StrongBox; never exported; per-key user-presence requirement | Done |
| 7 | Service API | Spoofed client identity | S | Client attestation per request; rate limit per device fingerprint; deny non-attested requests on sensitive endpoints (new device linking, identity-key publication) | Done |
| 8 | TB-3 data flow | TLS interception by system-CA mitm | T, I | Certificate pinning of leaf or intermediate; pin set rotated with app updates; degraded mode if pin fails (no key-material exchange) | Done |
| 9 | Service backend | Server compromise reveals message content | I | Messages stored as ciphertext only; server never sees plaintext; metadata minimisation (sealed-sender style envelopes); contact discovery via privacy-preserving protocol | Done |
| 10 | Service backend | Replay of stale ciphertext | T | Per-message counter and authenticated header; receiver rejects replays via ratchet state | Done |
| 11 | Service backend | DoS via spam / flood | D | Per-account rate limits; abuse-reporting flow; per-IP soft / hard caps; cost-bound proof of work on registration | Done |
| 12 | TB-4 push provider | Metadata disclosure via push | I | Payload encrypted client-side; provider sees only opaque ciphertext and a notification id; "silent" push for state-update events | Done |
| 13 | Device linking (QR) | Adversary-in-the-middle on pairing | S, T | Pairing payload includes verification short code displayed on both devices; user must confirm; per-pair channel keyed to the QR nonce | Done |
| 14 | TB-5 inter-app | Deep-link impersonation | S, T | App / universal links with verified domains only; reject unverified custom URL schemes for state-changing actions | Done |
| 15 | App | Forensic recovery of deleted messages | I | Disappearing-message TTL deletes ciphertext and ratchet state; secure delete of media; database stored with full-disk encryption protected by device unlock | Partial |

## Residual risks

- An attacker with physical access to an unlocked device can read
  conversations on that device. Detection and recovery are out of
  scope; offset with disappearing-message TTLs and biometric step-up
  for sensitive folders.
- A jailbroken / rooted device weakens many controls. Detection is
  best-effort; the app warns and refuses some operations (new device
  linking, identity-key change) on a detected rooted device.
- Metadata (who talked to whom, when, how often) is observable at the
  service layer. Sealed-sender style envelopes and private contact
  discovery reduce, but do not eliminate, this visibility.
- A coerced user can be made to perform any action under their
  biometric; offsetting controls are limited to UX (multi-step
  confirmation, decoy profile).

## Open questions

1. Is the pin set rotation cadence documented, and does the app fail
   open or closed when no fresh pin set is available within a defined
   staleness window?
2. Is the "disappearing message" TTL enforced symmetrically on every
   participant device, including older app versions, or is it
   advisory?
3. Does the abuse-reporting flow forward decrypted message content
   (by the reporter's consent) or only a sealed report? What is the
   retention?
4. Are pairing QR codes single-use, time-limited, and bound to the
   initiating account, so a leaked screenshot of a QR does not yield
   a linked device after the window?

## References

- OWASP MASVS: <https://mas.owasp.org/MASVS/>
- OWASP MASTG: <https://mas.owasp.org/MASTG/>
- Apple Platform Security — Secure Enclave: <https://support.apple.com/guide/security/secure-enclave-sec59b0b31ff/web>
- Android Keystore: <https://developer.android.com/training/articles/keystore>
- App Attest (Apple): <https://developer.apple.com/documentation/devicecheck/establishing_your_app_s_integrity>
- Play Integrity (Google): <https://developer.android.com/google/play/integrity>
- Signal Protocol — Double Ratchet (specification): <https://signal.org/docs/specifications/doubleratchet/>
- IETF Messaging Layer Security (MLS, RFC 9420): <https://datatracker.ietf.org/doc/html/rfc9420>
