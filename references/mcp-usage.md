# X Publisher MCP Usage

The curated MCP server is safe by default: `dry-run` mode previews mutating actions and never calls X.

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

Live X calls require explicit local config. For the broadest surface, use a separately configured official XMCP server:

```text
X_PUBLISHER_MODE=live
X_PUBLISHER_ALLOW_LIVE=1
X_PUBLISHER_BACKEND=xmcp
X_PUBLISHER_XMCP_URL=http://127.0.0.1:8000/mcp
```

For focused posting without an XMCP server, use the direct X API v2 backend:

```text
X_PUBLISHER_MODE=live
X_PUBLISHER_ALLOW_LIVE=1
X_PUBLISHER_BACKEND=x-api
X_PUBLISHER_X_USER_ACCESS_TOKEN=<user-context-token>
```

The direct backend supports create post, create thread by reply chaining, delete post, user lookup, and post lookup. Broader account-management operations should use `X_PUBLISHER_BACKEND=xmcp`.

The curated tools still require exact confirmation for posting, deleting, following, blocking, list changes, bookmarks, reposts, and likes.

## Browser Fallback

When API publishing fails because the account has no API credits, no eligible access tier, or a similar policy block, `create_post` and `create_thread` return:

```text
status=browser_fallback_available
```

Use the returned `browser_fallback` object:

- `kind=browser_post`: open `composer_url` in a signed-in browser, verify the visible account and text, then click Post.
- `kind=browser_thread`: open the first composer URL, post it, then use the browser reply composer on each posted item for later chunks.

Do not ask for passwords, 2FA codes, or cookies in chat. The user signs in locally; the agent operates only the browser session it can already see.
