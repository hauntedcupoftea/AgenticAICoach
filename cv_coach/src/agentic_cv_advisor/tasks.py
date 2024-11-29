from crewai import Task


def create_comprehensive_analysis_task(agent, cv_content):
    """
    Create a task for comprehensive CV analysis

    Args:
        agent (Agent): CV analysis agent
        cv_content (str): Content of the CV

    Returns:
        Task for comprehensive CV review
    """
    return Task(
        description=f"Perform a comprehensive analysis of the CV...",
        agent=agent,
        expected_output="""
        Detailed CV analysis including:
        - Structural strengths and weaknesses
        - Keyword optimization recommendations
        - Formatting and readability assessment
        - Suggestions for improvement
        """,
    )


def create_targeted_improvement_task(agent, query):
    """
    Create a task for targeted CV improvement

    Args:
        agent (Agent): Improvement agent
        query (str): Specific user question

    Returns:
        Task for targeted CV improvement
    """
    return Task(
        description=f"Address specific CV improvement query: {query}",
        agent=agent,
        expected_output="Specific, actionable recommendations addressing the user's query",
    )
