import os
from playwright.async_api import async_playwright
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from dotenv import load_dotenv
from langchain.agents import Tool
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_community.utilities import GoogleSerperAPIWrapper


load_dotenv(override=True)

# Headless by default (server/CI-friendly). Set HEADLESS=false to watch the browser.
HEADLESS = os.getenv("HEADLESS", "true").lower() != "false"

serper = GoogleSerperAPIWrapper()


async def playwright_tools():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=HEADLESS)
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=browser)
    return toolkit.get_tools(), browser, playwright


def get_file_tools():
    toolkit = FileManagementToolkit(root_dir="sandbox")
    return toolkit.get_tools()


async def other_tools():
    file_tools = get_file_tools()

    tool_search = Tool(
        name="search",
        func=serper.run,
        description="Use this tool when you want to get the results of an online web search",
    )

    return file_tools + [tool_search]
