"""Requirements tool for autonomous tester."""

from pathlib import Path
from chromadb.config import Settings
from crewai_tools import TXTSearchTool
from autonomous_tester.libs import settings



def _get_config():
    """Get configuration for the TXTSearchTool."""

    config={
        "embedding_model": {
            "provider": "azure",
            "config": {
                "api_base": settings.AZURE_API_BASE,
                "api_key": settings.AZURE_API_KEY,
                "api_version": settings.AZURE_API_VERSION,
                "deployment_id": settings.EMBEDDING_MODEL,
            },
        },
    }
    return config


def get_requirements(requirements_path: str) -> TXTSearchTool:
    """Get requirements from a file and add them to the vector database.
    
    Args:
        requirements_path (str): The path to the requirements file.
    
    Returns:
        TXTSearchTool: A tool that can be used to search the requirements.
    """
    path = Path(requirements_path)
    if not path.is_file():
        raise FileNotFoundError(f"Requirements file not found: {requirements_path}")

    requirements_tool = TXTSearchTool(
        txt=requirements_path,
        config=_get_config(),
    )
    return requirements_tool
