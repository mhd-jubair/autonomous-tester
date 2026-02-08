"""Browser tool for autonomous tester."""

import asyncio

from crewai.tools import BaseTool
from browser_use import BrowserProfile, ChatAzureOpenAI, Agent, Browser

from autonomous_tester.libs import settings


class BrowserTool(BaseTool):
    """Tool for performing browser related tasks in the autonomous tester."""

    name: str = "Browser task tool"
    description: str = "An asynchronous tool to perform browser related tasks."
    _browser: Browser | None = None

    def _get_llm(self) -> ChatAzureOpenAI:
        """Get the language model for the tool."""

        *_, llm_model = settings.MODEL.partition("/")
        llm = ChatAzureOpenAI(
            api_key = settings.AZURE_API_KEY,
            # api_version: str | None = '2024-10-21'
            azure_endpoint = settings.AZURE_API_BASE,
            model = llm_model
        )
        return llm

    async def _get_browser(self) -> Browser:
        """Get the browser instance for the tool."""
        if self._browser is None:
            self._browser = Browser(browser_profile=BrowserProfile(keep_alive=True))
            await self._browser.start()
        return self._browser
    
    async def _async_run(self, query: str = "") -> str:
        """Async implementation of the browser task.
        
        Args:
            query (str): The query describing the browser task to be performed.
        
        Returns:
            str: The result of the browser task.
        """
        browser = await self._get_browser()
        agent = Agent(task=query, llm=self._get_llm(), browser=browser)
        history = await agent.run()
        return history.action_results()[-1].extracted_content

    def _run(self, query: str = "") -> str:
        """Synchronous wrapper for CrewAI.
        
        Args:
            query (str): The query describing the browser task to be performed.
        
        Returns:
            str: The result of the browser task.
        """
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(self._async_run(query))

    def __del__(self):
        """Cleanup browser on tool destruction."""
        if self._browser is not None:
            try:
                loop = asyncio.get_event_loop()
                if not loop.is_closed():
                    loop.run_until_complete(self._browser.close())
            except Exception:
                pass
