"""Multi model AI Agentic crew for autonomous testing of software applications."""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

from autonomous_tester.libs import get_settings, Settings
from autonomous_tester.libs.crew_tools import tester_tools


@CrewBase
class AutonomousTester():
    """Crew for autonomous testing."""

    agents: List[BaseAgent]
    tasks: List[Task]
    settings: Settings = get_settings()

    agents_config = settings.AGENTS_CONFIG
    tasks_config = settings.TASKS_CONFIG

    @agent
    def test_planner(self) -> Agent:
        """Agent responsible for planning the testing strategy."""
        return Agent(
            config=self.agents_config['test_planner'],
            verbose=self.settings.VERBOSE,
            tools=[tester_tools.requirements_tool(self.settings.REQUIREMENTS_PATH)],
        )

    @agent
    def test_specialist(self) -> Agent:
        """Agent responsible for executing the tests."""
        return Agent(
            config=self.agents_config['test_specialist'],
            verbose=self.settings.VERBOSE,
            tools=[
                tester_tools.browser_tool,
                tester_tools.api_tool,
            ],
        )

    @agent
    def report_specialist(self) -> Agent:
        """Agent responsible for generating test reports."""
        return Agent(
            config=self.agents_config['report_specialist'],
            verbose=self.settings.VERBOSE,
        )

    @task
    def test_planning(self) -> Task:
        """Task for planning the testing strategy."""
        return Task(
            config=self.tasks_config['test_planning'],
        )

    @task
    def test_execution(self) -> Task:
        """Task for executing the tests."""
        return Task(
            config=self.tasks_config['test_execution'],
            context=[self.test_planning()],
        )
    
    @task
    def report_generation(self) -> Task:
        """Task for generating test reports."""
        return Task(
            config=self.tasks_config['report_generation'],
            context=[self.test_execution()],
            output_file="test_report.md",
            markdown=True
        )

    @crew
    def crew(self) -> Crew:
        """Crew for autonomous testing."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=self.settings.VERBOSE,
        )
