"""Init for the crew tools module."""

from .requirements_tool import get_requirements
from .browser_tool import BrowserTool
from .api_test_tool import APITestTool

from autonomous_tester.utils import DotDict


def get_tester_tools() -> DotDict:
    """Get all tools for the tester crew."""
    
    tool_collection = {
        "requirements_tool": get_requirements,
        "browser_tool": BrowserTool(),
        "api_tool": APITestTool(),
    }
    return DotDict(tool_collection)

tester_tools = get_tester_tools()


__all__ = [
    "tester_tools"
]
