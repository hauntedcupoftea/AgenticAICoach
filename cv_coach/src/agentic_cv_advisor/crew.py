from crewai import Crew, Process
from langchain_openai import ChatOpenAI
from dotenv import dotenv_values


def create_cv_review_crew(file_path):
    """
    Create a crew for comprehensive CV review and improvement

    Args:
        file_path (str): Path to the CV file to be reviewed

    Returns:
        Crew: Configured crew for CV analysis
    """
    config = dotenv_values(".env")
    # Initialize language model
    llm = ChatOpenAI(
        model_name="gpt-4", api_key=config["OPENAI_API_KEY"], temperature=0.3
    )

    # Import agents and create instances
    from agentic_cv_advisor.agent import (
        create_file_preprocessor_agent,
        create_structure_analysis_agent,
        create_keyword_analysis_agent,
        create_formatting_agent,
        create_content_quality_agent,
    )

    from agentic_cv_advisor.task import (
        create_preprocess_cv_task,
        create_structure_analysis_task,
        create_keyword_analysis_task,
        create_formatting_task,
        create_content_improvement_task,
    )

    # Create agents
    file_preprocessor = create_file_preprocessor_agent(llm)
    structure_analyst = create_structure_analysis_agent(llm)
    keyword_specialist = create_keyword_analysis_agent(llm)
    formatting_expert = create_formatting_agent(llm)
    content_enhancer = create_content_quality_agent(llm)

    # Create tasks
    preprocess_task = create_preprocess_cv_task(file_preprocessor, file_path)
    structure_task = create_structure_analysis_task(structure_analyst)
    keyword_task = create_keyword_analysis_task(keyword_specialist)
    formatting_task = create_formatting_task(formatting_expert)
    content_task = create_content_improvement_task(content_enhancer)

    # Configure and return crew
    return Crew(
        agents=[
            file_preprocessor,
            structure_analyst,
            keyword_specialist,
            formatting_expert,
            content_enhancer,
        ],
        tasks=[
            preprocess_task,
            structure_task,
            keyword_task,
            formatting_task,
            content_task,
        ],
        process=Process.sequential,
        verbose=2,
    )


def review_cv(file_path):
    """
    Main function to initiate CV review process

    Args:
        file_path (str): Path to the CV file

    Returns:
        Result of CV review process
    """
    cv_crew = create_cv_review_crew(file_path)
    return cv_crew.kickoff()
