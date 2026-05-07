# X Publisher

`x-publisher` is a lightweight Codex skill for drafting X posts, validating local character counts, splitting long drafts into threads, and opening prefilled X composer links.

V1 intentionally avoids direct API posting. It does not need X credentials.

## Install Locally

From the source repo:

```powershell
python tools/install_local.py
```

This copies the runtime skill files into:

```text
C:\Users\ngaremuki\.codex\skills\x-publisher
```

## CLI

```powershell
python scripts/x_publish.py draft --text "Shipped x-publisher v1."
python scripts/x_publish.py validate --text "Shipped x-publisher v1." --url "https://github.com/iice257/x-publisher"
python scripts/x_publish.py intent --text "Shipped x-publisher v1." --url "https://github.com/iice257/x-publisher"
python scripts/x_publish.py thread --file post.md
```

Add `--open` to `intent` to open the generated composer URL in the default browser.

## V2 Direction

X now has an official XMCP server. V2 should build on or wrap that official MCP/OpenAPI surface and add safer agent workflows for posting, account context, search, and management.
