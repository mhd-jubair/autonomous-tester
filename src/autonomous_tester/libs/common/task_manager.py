"""Task manager for test execution."""

import yaml
from autonomous_tester.libs import settings


def _load_task_collections() -> dict:
    """Load task collections from the configuration file.
    
    Returns:
        dict: A dictionary containing task collections.
    """

    with open(settings.TASK_COLLECTIONS, "r") as file:
        task_collections = yaml.safe_load(file)
    return task_collections


def manage_tasks(type: str, **kwargs) -> str:
    """Manage and monitor tasks during test execution.
    
    Args:
        type (str): The type of application to be tested (e.g., web_app,
        **kwargs: Additional keyword arguments for task management (e.g., endpoint).
    
    Returns:
        str: The task description for the specified application type.
    """

    task_collections = _load_task_collections()
    task = task_collections.get(type)

    if task is None:
        raise ValueError(f"Unsupported application type: {type}")

    task = task.format(**kwargs)
    return task
