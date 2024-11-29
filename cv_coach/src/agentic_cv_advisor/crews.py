from agentic_cv_advisor.agents import (
    create_cv_analysis_agent,
    create_targeted_improvement_agent,
)
from agentic_cv_advisor.tasks import (
    create_comprehensive_analysis_task,
    create_targeted_improvement_task,
)
from crewai import Crew, Process
from langchain_openai import ChatOpenAI


def create_cv_review_crew(cv_content, query=None):
    """Create a crew for CV review and improvement"""
    # Initialize language model
    llm = ChatOpenAI(model_name="gpt-4", temperature=0.3)

    # Create agents
    analysis_agent = create_cv_analysis_agent(llm, cv_content)

    # Create tasks
    comprehensive_task = create_comprehensive_analysis_task(analysis_agent, cv_content)

    # If a specific query is provided, create a targeted improvement task
    targeted_tasks = []
    if query:
        improvement_agent = create_targeted_improvement_agent(llm, cv_content, query)
        targeted_task = create_targeted_improvement_task(improvement_agent, query)
        targeted_tasks.append(targeted_task)

    # Configure and return crew
    return Crew(
        agents=[analysis_agent],
        tasks=[comprehensive_task] + targeted_tasks,
        process=Process.sequential,
        verbose=True,
    )


def review_cv(cv_content, query=None):
    """Main function to initiate CV review process"""
    cv_crew = create_cv_review_crew(cv_content, query)
    return cv_crew.kickoff()
