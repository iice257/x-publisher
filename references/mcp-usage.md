# X Publisher MCP Usage

V2 adds a curated MCP server in the source repo. It is safe by default: `dry-run` mode previews mutating actions and never calls X.

## Start

Install dependencies when you need to run the actual MCP server:

```powershell
python -m pip install -r requirements.txt
```

List tools without starting the server:

```powershell
python -m x_publisher_mcp.server --list-tools
```

Start the local MCP server:

```powershell
python -m x_publisher_mcp.server
```

Default endpoint:

```text
http://127.0.0.1:8765/mcp
```

## Live Backend

Live X calls require a separately configured official XMCP server and explicit local config:

```text
X_PUBLISHER_MODE=live
X_PUBLISHER_ALLOW_LIVE=1
X_PUBLISHER_XMCP_URL=http://127.0.0.1:8000/mcp
```

The curated tools still require exact confirmation for posting, deleting, following, blocking, list changes, bookmarks, reposts, and likes.
