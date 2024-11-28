from crewai import Agent

def create_learning_CV_coach(tools, llm_gpt4o):
    """
    Creates a learning CV coach agent responsible for searching through CVs (.CV/.docx) and
    answering user questions based on the contents of those documents.

    Args:
        tools (list): List of tools that the agent will use, such as PDFSearchTool for document searching.
        llm_gpt4o (LLM): The language model instance (e.g., GPT-4) that the agent uses for generating responses.

    Returns:
        Agent: The initialized agent configured to handle CV search tasks and respond to user queries.
    """
    return Agent(
        role="Document Search Agent",
        goal="Search through all uploaded documents to find relevant answers.",
        backstory="An agent adept at searching and extracting data from multiple documents.",
        tools=tools,
        max_execution_time=300,
        verbose=True,
        llm=llm_gpt4o
    )
