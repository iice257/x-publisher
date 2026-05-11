# X Publisher

`x-publisher` is a Codex skill and MCP runtime for X/Twitter publishing workflows.

It supports two paths:

- Local draft/composer workflow: draft, validate, split into threads, and open prefilled X composer links.
- MCP workflow: dry-run-first tools for posting, thread creation, deletes, lookups, and account-management delegation through either the direct X API backend or an official XMCP backend.

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
python scripts/x_publish.py draft --text "Shipped x-publisher: local drafts plus a dry-run-first MCP posting path."
python scripts/x_publish.py validate --text "Shipped x-publisher." --url "https://github.com/iice257/x-publisher"
python scripts/x_publish.py intent --text "Shipped x-publisher." --url "https://github.com/iice257/x-publisher"
python scripts/x_publish.py thread --file post.md
```

Add `--open` to `intent` to open the generated composer URL in the default browser.

## MCP Runtime

List tools:

```powershell
python -m x_publisher_mcp.server --list-tools
```

Run the MCP server:

```powershell
python -m pip install -r requirements.txt
python -m x_publisher_mcp.server
```

Default endpoint:

```text
http://127.0.0.1:8765/mcp
```

The MCP server defaults to `dry-run`; mutating tools require an exact confirmation string and do not call X unless live mode is explicitly enabled.

Live mode can use either a separately configured official XMCP backend or the focused direct X API backend for create/delete/read basics:

```powershell
$env:X_PUBLISHER_MODE="live"
$env:X_PUBLISHER_ALLOW_LIVE="1"
$env:X_PUBLISHER_BACKEND="x-api"
$env:X_PUBLISHER_X_USER_ACCESS_TOKEN="<user-context-token>"
python -m x_publisher_mcp.server
```

The direct backend uses X API v2 `POST /2/tweets` for posting. Keep tokens in local environment variables only.

## Full Account-Management Surface

X now has an official XMCP server. Use `X_PUBLISHER_BACKEND=xmcp` when the task needs broader account-management operations beyond the direct backend's focused create/delete/read basics.
