"""Configuration for the autonomous tester.

Info:
    Environmental variables starts with prefix `AT` states that they are related to the autonomous tester configuration. For example, `AT_VERBOSE` is an environmental variable that controls the verbosity of the autonomous tester.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class BASE:
    """Base configuration for the autonomous tester."""

    BASE_DIR = "src/autonomous_tester/"
    CONFIG_BASE = "config/"

    WEBAPP_REQUIREMENTS_PATH = "example/web_app/web_application.txt"
    API_REQUIREMENTS_PATH = "example/api/API_application.txt"


class Settings:
    """Settings for the autonomous tester."""

    VERBOSE: bool = os.getenv("AT_VERBOSE", "False").lower() in ("true", "1", "t")
    REQUIREMENTS_PATH = os.getenv("AT_REQUIREMENTS_PATH", BASE.API_REQUIREMENTS_PATH)

    AGENTS_CONFIG = BASE.CONFIG_BASE + "agents.yaml"
    TASKS_CONFIG = BASE.CONFIG_BASE + "tasks.yaml"
    TASK_COLLECTIONS = BASE.BASE_DIR + "tester_crew/config/" + "task_collections.yaml"

    STORAGE_DIR = ".memory/"

    def __init__(self):
        for key, value in os.environ.items():
            setattr(self, key, value)
