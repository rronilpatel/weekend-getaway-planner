from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class WeekendGetawayPlanner:
    """Weekend Getaway Planner crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def itinerary_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['itinerary_planner'],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def budget_checker(self) -> Agent:
        return Agent(
            config=self.agents_config['budget_checker'],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def travel_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['travel_writer'],  # type: ignore[index]
            verbose=True,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_destinations'],  # type: ignore[index]
        )

    @task
    def itinerary_task(self) -> Task:
        return Task(
            config=self.tasks_config['create_itinerary'],  # type: ignore[index]
        )

    @task
    def budget_task(self) -> Task:
        return Task(
            config=self.tasks_config['validate_budget_logistics'],  # type: ignore[index]
        )

    @task
    def writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['write_final_guide'],  # type: ignore[index]
            # Optional: output_file='final_guide.md'  # saves output automatically
        )

    @crew
    def crew(self) -> Crew:
        """Creates the WeekendGetawayPlanner crew"""
        return Crew(
            agents=self.agents,   # auto-populated by @agent decorators
            tasks=self.tasks,     # auto-populated by @task decorators
            process=Process.sequential,
            verbose=True,            # higher verbosity = see more agent conversation
            # memory=True,        # optional - enable if you want short-term memory
            # process=Process.hierarchical,  # try later if you want a manager agent
        )

    @before_kickoff
    def prepare_inputs(self, inputs):
        """Optional: modify or validate inputs before crew starts"""
        print("Before kickoff → inputs:", inputs)
        # You could add defaults here if missing
        inputs.setdefault("home_city", "Halifax, Nova Scotia")
        inputs.setdefault("budget", "medium ($400–800 CAD total)")
        inputs.setdefault("interests", "nature, seafood, relaxing")
        return inputs

    @after_kickoff
    def finalize(self, result):
        print("After kickoff → final result received")
        return result