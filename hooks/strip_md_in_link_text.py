"""
Strip a trailing `.md` from inline markdown link text only.

The READMEs across this handbook use `[filename.md](filename.md)` so that
GitHub's own renderer shows a recognisable file name in the source-view
list. On the mkdocs-material site that reads as cruft. This hook rewrites
the link *text* (not the URL) at build time, leaving the source files
intact for GitHub.

Registered from mkdocs.yml as:

    hooks:
      - hooks/strip_md_in_link_text.py
"""

import re

# Matches an inline link `[text.md](url)` where `text` contains no `]`
# and no newline. The URL part is captured but left untouched.
_LINK_TEXT_DOT_MD = re.compile(r"\[([^\]\n]+?)\.md\]")


def on_page_markdown(markdown: str, **kwargs) -> str:
    return _LINK_TEXT_DOT_MD.sub(lambda m: f"[{m.group(1)}]", markdown)
