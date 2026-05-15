# wraith-mcp

[![PyPI](https://img.shields.io/pypi/v/wraith-mcp)](https://pypi.org/project/wraith-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

AI-native stealth browser MCP server. Tell it what to do — it figures out how.

[Browser Use](https://github.com/browser-use/browser-use) (AI vision navigation) + [Patchright](https://github.com/Kaliiiiiiiiii-Vinyzu/patchright) (bot detection bypass).

## Why This One?

| | wraith-mcp | playwright-mcp | stealth-browser-mcp | browser-use-mcp-server |
|---|---|---|---|---|
| Navigation | **AI vision** (self-healing) | CSS selectors | CSS selectors | AI vision |
| Bot detection bypass | **Patchright** (binary-level) | None | nodriver | None |
| Tools | 6 (`browse`, `extract`, `screenshot`, sessions) | 20+ | 90+ | via Agent |
| Site layout changes | **Adapts automatically** | Breaks | Breaks | Adapts |
| LLM providers | **6** (Anthropic, OpenAI, OpenRouter, Google, Ollama, +compatible) | N/A | 1 | 1 |

**One command does it all** — no selectors, no step-by-step scripting:

```
"Log into my dashboard and download the monthly report"
```

## Quick Start

> Add wraith-mcp as MCP server

## Install

```bash
pip install wraith-mcp
```

## Setup

Add to your MCP config (`.mcp.json`, `.cursor/mcp.json`, `.windsurf/mcp.json`, etc.):

```json
{
  "mcpServers": {
    "wraith": {
      "command": "wraith-mcp",
      "env": {
        "HEADLESS": "true"
      }
    }
  }
}
```

Works with any MCP client: Cursor, Windsurf, VS Code, Cline, Roo Code, OpenCode, Codex, and more.

These clients call Wraith over MCP. When the client supports MCP sampling,
Wraith can ask that already logged-in client model to drive Browser Use, so no
separate Wraith API key is needed.

## Do I Need an API Key?

Not when your MCP client supports sampling/createMessage.

Wraith's preferred keyless path is MCP sampling: the MCP client mediates model
calls using its own logged-in model session. Wraith does not read Codex, Claude
Code, or OpenCode OAuth tokens directly.

If your client does not support sampling, configure a fallback provider such as
`OPENROUTER_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, or
local Ollama via `OLLAMA_MODEL`. Do not paste Codex login/OAuth as
`OPENAI_API_KEY`; it is not an API-key credential.

## Tools

| Tool | Description |
|------|-------------|
| `browse` | Execute any browser task in natural language |
| `extract` | Pull structured data from a page |
| `screenshot` | Capture a page as base64 PNG |
| `list_sessions` | List active persistent browser session IDs |
| `close_session` | Close a persistent browser session |
| `close_all_sessions` | Close all active persistent browser sessions |

`browse` and `extract` support optional `session_id` for persistent browser
sessions across multiple calls. Use `list_sessions`, `close_session`, and
`close_all_sessions` to manage those sessions.

## Fallback LLM Providers

Use these only when your MCP client does not support sampling, or when you want
to force Wraith to use an explicit provider.

| Provider | Key |
|----------|-----|
| Anthropic (default) | `ANTHROPIC_API_KEY` |
| OpenRouter | `OPENROUTER_API_KEY` |
| OpenAI | `OPENAI_API_KEY` |
| DeepSeek / Groq / Together | `OPENAI_API_KEY` + `OPENAI_BASE_URL` |
| Google Gemini | `GOOGLE_API_KEY` |
| Ollama (local) | `OLLAMA_MODEL` |

Set `BROWSER_USE_MODEL` to override the default model or provide a sampling model
hint to the MCP client.

## Browser Options

Wraith keeps its default browser profile unless optional env vars are set. It can
forward Browser Use profile knobs for domain policy (`BROWSER_ALLOWED_DOMAINS`,
`BROWSER_PROHIBITED_DOMAINS`, `BROWSER_BLOCK_IP_ADDRESSES=true` for Browser
Use's direct-IP navigation block), session/artifacts (`BROWSER_STORAGE_STATE`,
`BROWSER_USER_DATA_DIR`, `BROWSER_DOWNLOADS_PATH`, `BROWSER_RECORD_HAR_PATH`,
`BROWSER_RECORD_VIDEO_DIR`, `BROWSER_TRACES_DIR`), and permissions, viewport, or
wait timing (`BROWSER_PERMISSIONS`, `BROWSER_VIEWPORT`,
`BROWSER_MINIMUM_WAIT_PAGE_LOAD_TIME`,
`BROWSER_WAIT_FOR_NETWORK_IDLE_PAGE_LOAD_TIME`, `BROWSER_WAIT_BETWEEN_ACTIONS`)
when the installed Browser Use `BrowserProfile` supports those fields. Domain/IP
policy env vars fail closed on unsupported Browser Use versions.

## Docker

```bash
docker build -t wraith-mcp .
docker run -i --rm wraith-mcp
```

SSE mode for local-only testing:

```bash
docker run -p 127.0.0.1:8808:8808 wraith-mcp --transport sse --host 0.0.0.0 --port 8808
```

Do not expose the SSE port directly to an untrusted network. If you need remote
access, put it behind an authenticated proxy or SSH tunnel and restrict browsing
with `BROWSER_ALLOWED_DOMAINS` plus `BROWSER_BLOCK_IP_ADDRESSES=true`.

## SSE Transport

```bash
wraith-mcp --transport sse --host 127.0.0.1 --port 8808
```

The SSE host defaults to `127.0.0.1`. Binding to `0.0.0.0` is only appropriate
behind an authenticated proxy or another trusted network boundary.

## How It Works

```
AI Agent -> MCP Server -> Browser Use Agent -> Patchright Chromium
```

1. Describe a task in natural language
2. Browser Use asks the MCP client model through sampling, or a fallback provider
3. Browser Use sees the page (screenshot + DOM) and decides actions
4. Patchright executes without triggering bot detection

## Security

- URL scheme validation (http/https only)
- `max_steps` capped at 50 server-side
- Input length capped at 4000 chars
- Task timeout (default 120s, configurable via `BROWSER_TASK_TIMEOUT`)
- Proxy support via `PROXY_SERVER`
- SSE transport binds to `127.0.0.1` by default; do not expose it directly
  without authentication
- Browser Use page context is sent to the MCP client model via sampling, or to
  the configured fallback provider

## Limitations

- Binary-level stealth only (no `Runtime.enable` CDP fix)
- Enterprise WAFs may still block without residential proxies
- Fresh browser per call (~3s startup)
- Keyless mode requires an MCP client with sampling/createMessage support
- Sampling support varies by MCP client; use a fallback provider or Ollama when unsupported

## License

MIT
