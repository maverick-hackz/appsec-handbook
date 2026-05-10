# Reading List

Books, papers, and long-form sources. One line per entry explaining
why it earns space on a shelf.

## Books -- application security

- **The Web Application Hacker's Handbook (2nd ed.)** -- Dafydd
  Stuttard, Marcus Pinto, 2011. Encyclopedic web pentest reference;
  the WSTG superset.
- **Real-World Cryptography** -- David Wong, 2021. Modern crypto from
  AEAD and TLS 1.3 to post-quantum, with reasoning rather than
  formulas.
- **Cryptography Engineering** -- Niels Ferguson, Bruce Schneier,
  Tadayoshi Kohno, 2010. Practical crypto-protocol design.
- **Black Hat Python (2nd ed.)** -- Justin Seitz, Tim Arnold, 2021.
  Pythonic tooling for offensive engineering and security automation.

## Books -- secure software development

- **Threat Modeling: Designing for Security** -- Adam Shostack, 2014.
  The reference text for STRIDE; required if the team does any
  structured threat modeling.
- **Designing Secure Software** -- Loren Kohnfelder, 2021. Modern
  secure-design patterns; complements Shostack.
- **The Tangled Web** -- Michal Zalewski, 2011. The browser security
  model from the ground up; still relevant.
- **Building Secure and Reliable Systems** -- Heather Adkins et al.
  (Google SRE Book), 2020. Operating large-scale systems with
  security as a property, not a bolt-on.

## Books -- DevSecOps and supply chain

- **Securing DevOps** -- Julien Vehent, 2018. End-to-end DevOps with
  security woven through; AWS-flavoured but transferable.
- **The DevSecOps Handbook** -- Gene Kim et al., 2018. Process side
  of "shift left"; pairs with the technical resources.
- **Cybersecurity Supply Chain Risk Management** -- Jon Boyens et al.,
  NIST SP 800-161 commentary. <!-- TODO: verify the most current
  edition / commentary; cite the NIST publication directly. -->

## Papers and long-form research

- **"On Breaking SAML: Be Whoever You Want to Be"** -- Somorovsky et
  al., USENIX Security 2012. Canonical reference for SAML signature
  wrapping.
- **"Why Cryptosystems Fail"** -- Ross Anderson, ACM 1993. Aging but
  formative: the bugs are usually outside the cryptography.
- **"Attack Trees"** -- Bruce Schneier, Dr. Dobb's Journal 1999.
  Source paper for the attack-tree methodology.
- **The Memory-Safe Roadmap** -- ONCD / CISA. Statement on why
  memory-safe languages matter at the national-policy level.

## Research blogs (primary sources)

- **Project Zero (Google)** -- <https://googleprojectzero.blogspot.com/>
  -- platform-level vulnerability disclosure with deep root-cause
  writeups.
- **PortSwigger Research** -- <https://portswigger.net/research> --
  novel web-attack techniques (James Kettle and team).
- **NCC Group Research** -- <https://research.nccgroup.com/> --
  protocol audits, cryptographic reviews, deep technical writeups.
- **Trail of Bits Blog** -- <https://blog.trailofbits.com/> -- platform
  and language-level security research.
- **Doyensec Blog** -- <https://blog.doyensec.com/> -- application
  security findings and tooling.
- **OWASP Blog** -- <https://owasp.org/news/> -- standards and project
  releases (ASVS, SAMM, MASVS).
- **CNCF Security TAG** -- <https://github.com/cncf/tag-security> --
  cloud-native security guidance and whitepapers.

## How to read

- Start broad (Shostack, Stuttard) before going deep (Wong, Ferguson).
- Pair each book with a real project: build a threat model for a
  team's service after Shostack; implement one entry from the
  Cryptography Engineering chapters in Go after Ferguson.
- Subscribe to one or two research blogs and read them in batches,
  not in a feed reader. The signal is the patterns, not every post.
