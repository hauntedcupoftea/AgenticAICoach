from crewai import Agent


def create_file_preprocessor_agent(tools, llm):
    return Agent(
        role="CV File Preprocessor",
        goal="Convert uploaded CVs to a standardized format for analysis",
        backstory="Expert in document conversion and resume standardization",
        tools=tools,
        verbose=True,
        llm=llm,
    )


def create_structure_analysis_agent(llm):
    return Agent(
        role="CV Structure Analyst",
        goal="Evaluate CV structure and section completeness",
        backstory="Professional recruiter specializing in resume optimization",
        verbose=True,
        llm=llm,
    )


def create_keyword_analysis_agent(llm):
    return Agent(
        role="Industry Keyword Specialist",
        goal="Analyze and suggest industry-specific keywords",
        backstory="Recruitment expert with deep understanding of keyword optimization",
        verbose=True,
        llm=llm,
    )


def create_formatting_agent(llm):
    return Agent(
        role="CV Formatting Expert",
        goal="Assess and recommend CV formatting improvements",
        backstory="Design professional with expertise in resume visual presentation",
        verbose=True,
        llm=llm,
    )


def create_content_quality_agent(llm):
    return Agent(
        role="Content Quality Enhancer",
        goal="Improve CV content quality and professional language",
        backstory="Senior career coach specializing in resume writing",
        verbose=True,
        llm=llm,
    )
