from crewai import Agent
from crewai_tools import DOCXSearchTool, PDFSearchTool


def create_cv_analysis_agent(llm, cv_content):
    """Create an agent for comprehensive CV analysis"""
    # Configure search tools with CV content
    pdf_tool = PDFSearchTool(pdf=str(cv_content))
    docx_tool = DOCXSearchTool(docx=str(cv_content))

    return Agent(
        role="CV Review Specialist",
        goal=f"Comprehensively analyze and improve the CV.",
        backstory="Expert career coach specializing in transforming CVs into powerful career marketing documents",
        tools=[pdf_tool, docx_tool],
        verbose=True,
        llm=llm,
    )


def create_targeted_improvement_agent(llm, cv_content, query):
    """Create an agent for targeted CV improvement"""
    # Configure search tools with CV content
    pdf_tool = PDFSearchTool(content=cv_content)
    docx_tool = DOCXSearchTool(content=cv_content)

    return Agent(
        role="CV Improvement Consultant",
        goal=f"Provide specific guidance on: {query}",
        backstory="Seasoned recruitment professional with expertise in tailoring CVs to specific career goals",
        tools=[pdf_tool, docx_tool],
        verbose=True,
        llm=llm,
    )
