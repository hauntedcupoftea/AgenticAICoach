from crewai import Task


def create_preprocess_cv_task(agent, file_path):
    return Task(
        description=f"Preprocess the CV located at {file_path}",
        agent=agent,
        expected_output="Extracted and standardized CV content ready for further analysis",
    )


def create_structure_analysis_task(agent):
    return Task(
        description="Analyze CV structure and section completeness",
        agent=agent,
        expected_output="""
        Detailed report including:
        - Completeness of sections
        - Missing critical sections
        - Structural recommendations
        - Section scoring
        """,
    )


def create_keyword_analysis_task(agent):
    return Task(
        description="Perform industry-specific keyword analysis",
        agent=agent,
        expected_output="""
        Keyword analysis report:
        - Missing industry keywords
        - Keyword density recommendations
        - Integration suggestions
        """,
    )


def create_formatting_task(agent):
    return Task(
        description="Review CV formatting and visual presentation",
        agent=agent,
        expected_output="""
        Formatting assessment:
        - Font consistency
        - Spacing and alignment
        - Section header formatting
        - Readability recommendations
        """,
    )


def create_content_improvement_task(agent):
    return Task(
        description="Enhance CV content quality and professional language",
        agent=agent,
        expected_output="""
        Content quality report:
        - Action verb assessment
        - Achievement quantification
        - Language professionalism scoring
        - Writing improvement suggestions
        """,
    )
