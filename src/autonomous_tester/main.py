"""Main script for the autonomous tester."""

import argparse
from typing import Literal
from autonomous_tester.tester_crew.tester_crew import AutonomousTester
from autonomous_tester.libs.common.task_manager import manage_tasks


def main(type: str, **kwargs):
    """Main function to run the autonomous tester.
    
    Args:
        type (str): The type of application to be tested (e.g., web_app, api_app).
        **kwargs: Additional keyword arguments for task management (e.g., endpoint).
    """
    inputs = {
        "task_description": manage_tasks(type, **kwargs)
    }

    autonomous_tester = AutonomousTester().crew()
    autonomous_tester.kickoff(inputs=inputs)


if __name__ == "__main__":
    """Main entry point for the autonomous tester."""

    parser = argparse.ArgumentParser(description="Run the autonomous tester.")

    parser.add_argument(
        "--type",
        type=str,
        choices=["web_app", "api_app"],
        required=True,
        help="Application type (e.g., web_app, api_app).",
    )

    parser.add_argument(
        "--endpoint",
        type=str,
        required=True,
        help="The endpoint of the web application to be tested (e.g., http://localhost:8000).",
    )
    args = parser.parse_args()
    main(args.type, endpoint=args.endpoint)
