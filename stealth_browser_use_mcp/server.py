"""Stealth Browser Use MCP Server — AI-native browser automation with bot detection evasion."""

import os
from urllib.parse import urlparse

from mcp.server.fastmcp import FastMCP
from browser_use import Agent
from browser_use.browser.profile import BrowserProfile
from browser_use.browser.session import BrowserSession
from langchain_core.language_models import BaseChatModel

from .browser_manager import chromium_path

mcp = FastMCP(
    "stealth-browser-use",
    instructions=(
        "AI-native stealth browser. Send natural language tasks — "
        "no selectors needed. Resilient to site layout changes."
    ),
)

_ALLOWED_SCHEMES = {"http", "https"}
_MAX_STEPS_LIMIT = 50
_MAX_INPUT_LENGTH = 4000
_DEFAULT_ANTHROPIC_MODEL = "claude-sonnet-4-20250514"
_DEFAULT_OPENAI_MODEL = "gpt-4o"


def _validate_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in _ALLOWED_SCHEMES:
        raise ValueError(
            f"URL scheme '{parsed.scheme}' is not allowed. Only http/https are permitted."
        )
    return url


def _clamp_steps(max_steps: int) -> int:
    return min(max(1, max_steps), _MAX_STEPS_LIMIT)


def _llm() -> BaseChatModel:
    if os.environ.get("OPENAI_API_KEY"):
        try:
            from langchain_openai import ChatOpenAI
        except ImportError as e:
            raise ImportError(
                "OPENAI_API_KEY is set but langchain-openai is not installed. "
                "Run: pip install 'stealth-browser-use-mcp[openai]'"
            ) from e
        model = os.environ.get("BROWSER_USE_MODEL", _DEFAULT_OPENAI_MODEL)
        return ChatOpenAI(model=model)

    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise RuntimeError(
            "No LLM API key found. Set ANTHROPIC_API_KEY or OPENAI_API_KEY."
        )

    from langchain_anthropic import ChatAnthropic

    model = os.environ.get("BROWSER_USE_MODEL", _DEFAULT_ANTHROPIC_MODEL)
    return ChatAnthropic(model=model)


def _profile() -> BrowserProfile:
    headless = os.environ.get("HEADLESS", "true").lower() == "true"
    return BrowserProfile(
        executable_path=chromium_path(),
        headless=headless,
    )


@mcp.tool()
async def browse(task: str, url: str | None = None, max_steps: int = 25) -> str:
    """Execute a browser task described in natural language.
    The AI agent navigates and interacts with pages automatically.
    Resilient to site layout changes — no CSS selectors needed.

    Args:
        task: What to do, e.g. "Search for 'AI news' and return top 3 results"
        url: Optional starting URL to navigate to first
        max_steps: Maximum interaction steps (capped at 50)
    """
    if len(task) > _MAX_INPUT_LENGTH:
        raise ValueError(f"Task too long ({len(task)} chars). Max {_MAX_INPUT_LENGTH}.")

    full_task = task
    if url:
        full_task = f"Go to {_validate_url(url)}. Then: {task}"

    session = BrowserSession(browser_profile=_profile())
    async with session:
        agent = Agent(task=full_task, llm=_llm(), browser_session=session)
        result = await agent.run(max_steps=_clamp_steps(max_steps))
        return result.final_result() or "Task completed, no text result."


@mcp.tool()
async def extract(url: str, data_description: str, max_steps: int = 15) -> str:
    """Extract structured data from a webpage using natural language.

    Args:
        url: Target URL
        data_description: What to extract, e.g. "all product names and prices in JSON"
        max_steps: Maximum interaction steps (capped at 50)
    """
    if len(data_description) > _MAX_INPUT_LENGTH:
        raise ValueError(
            f"Description too long ({len(data_description)} chars). Max {_MAX_INPUT_LENGTH}."
        )

    task = (
        f"Go to {_validate_url(url)}. "
        f"Extract the following data and return it in a structured format: {data_description}"
    )

    session = BrowserSession(browser_profile=_profile())
    async with session:
        agent = Agent(task=task, llm=_llm(), browser_session=session)
        result = await agent.run(max_steps=_clamp_steps(max_steps))
        return result.final_result() or "No data extracted."


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
