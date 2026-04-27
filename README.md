# stealth-browser-use-mcp

[![PyPI](https://img.shields.io/pypi/v/stealth-browser-use-mcp)](https://pypi.org/project/stealth-browser-use-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

AI-native stealth browser MCP server. Tell it what to do — it figures out how.

[Browser Use](https://github.com/browser-use/browser-use) (AI vision navigation) + [Patchright](https://github.com/Kaliiiiiiiiii-Vinyzu/patchright) (bot detection bypass).

## Why This One?

| | stealth-browser-use-mcp | playwright-mcp | stealth-browser-mcp | browser-use-mcp-server |
|---|---|---|---|---|
| Navigation | **AI vision** (self-healing) | CSS selectors | CSS selectors | AI vision |
| Bot detection bypass | **Patchright** (binary-level) | None | nodriver | None |
| Tools | 2 (`browse`, `extract`) | 20+ | 90+ | via Agent |
| Site layout changes | **Adapts automatically** | Breaks | Breaks | Adapts |
| LLM providers | **6** (Anthropic, OpenAI, OpenRouter, Google, Ollama, +compatible) | N/A | 1 | 1 |

**One command does it all** — no selectors, no step-by-step scripting:

```
"Log into my dashboard and download the monthly report"
```

## Quick Start

> Add stealth-browser-use-mcp as MCP server

## Install

```bash
pip install stealth-browser-use-mcp
```

## Setup

Add to your MCP config (`.mcp.json`, `.cursor/mcp.json`, `.windsurf/mcp.json`, etc.):

```json
{
  "mcpServers": {
    "stealth-browser": {
      "command": "stealth-browser-use-mcp",
      "env": {
        "ANTHROPIC_API_KEY": "your-key",
        "HEADLESS": "true"
      }
    }
  }
}
```

Works with any MCP client: Cursor, Windsurf, VS Code, Cline, Roo Code, OpenCode, Codex, and more.

## Tools

| Tool | Description |
|------|-------------|
| `browse` | Execute any browser task in natural language |
| `extract` | Pull structured data from a page |

## LLM Providers

| Provider | Key |
|----------|-----|
| Anthropic (default) | `ANTHROPIC_API_KEY` |
| OpenRouter | `OPENROUTER_API_KEY` |
| OpenAI | `OPENAI_API_KEY` |
| DeepSeek / Groq / Together | `OPENAI_API_KEY` + `OPENAI_BASE_URL` |
| Google Gemini | `GOOGLE_API_KEY` |
| Ollama (local) | `OLLAMA_MODEL` |

All providers included. Set `BROWSER_USE_MODEL` to override the default model.

## How It Works

```
AI Agent -> MCP Server -> Browser Use Agent -> Patchright Chromium
```

1. Describe a task in natural language
2. Browser Use sees the page (screenshot + DOM) and decides actions
3. Patchright executes without triggering bot detection

## Docker

```bash
docker build -t stealth-browser-use-mcp .
docker run -i --rm -e ANTHROPIC_API_KEY=your-key stealth-browser-use-mcp
```

SSE mode (remote/cloud):

```bash
docker run -p 8808:8808 -e ANTHROPIC_API_KEY=your-key stealth-browser-use-mcp
```

## SSE Transport

```bash
stealth-browser-use-mcp --transport sse --port 8808
```

## Security

- URL scheme validation (http/https only)
- `max_steps` capped at 50 server-side
- Input length capped at 4000 chars
- Task timeout (default 120s, configurable via `BROWSER_TASK_TIMEOUT`)
- Proxy support via `PROXY_SERVER`

## Limitations

- Binary-level stealth only (no `Runtime.enable` CDP fix)
- Enterprise WAFs may still block without residential proxies
- Fresh browser per call (~3s startup)
- Requires an LLM API key

## License

MIT
