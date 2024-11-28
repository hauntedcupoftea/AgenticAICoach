from crewai import Agent, Task, Crew
from langchain.llms import OpenAI


class CVCoachAgents:
    def __init__(self, cv_content):
        # Initialize the language model
        self.llm = OpenAI(temperature=0.7)
        self.cv_content = cv_content

    def content_extractor_agent(self):
        return Agent(
            role="CV Content Extractor",
            goal="Extract and organize key information from the CV",
            backstory="You are an expert at parsing professional documents and identifying critical career information",
            verbose=True,
            llm=self.llm,
            allow_delegation=False,
        )

    def cv_scoring_agent(self):
        return Agent(
            role="CV Scoring Specialist",
            goal="Provide a comprehensive scoring and analysis of CV sections",
            backstory="You are a seasoned hiring manager and career coach who can critically evaluate CVs across multiple dimensions",
            verbose=True,
            llm=self.llm,
            allow_delegation=True,
        )

    def improvement_recommendation_agent(self):
        return Agent(
            role="CV Improvement Coach",
            goal="Generate specific, actionable recommendations to enhance CV sections",
            backstory="You are a professional resume writer with expertise in helping candidates optimize their career documents",
            verbose=True,
            llm=self.llm,
            allow_delegation=False,
        )

    def create_cv_analysis_crew(self):
        # Extract content task
        extract_task = Task(
            description=f"""
            Carefully extract and organize all key information from the following CV into a JSONResume:
            {self.cv_content}
            """,
            agent=self.content_extractor_agent(),
            expected_output="Structured summary of CV content",
        )

        # Scoring task
        scoring_task = Task(
            description="""
            Provide a detailed scoring of the CV across these key dimensions:
            1. Overall professional presentation (0-10)
            2. Clarity of career progression (0-10)
            3. Relevance of skills to target industry (0-10)
            4. Achievement highlighting (0-10)
            5. Formatting and readability (0-10)
            
            Include specific rationale for each score.
            """,
            agent=self.cv_scoring_agent(),
            expected_output="Comprehensive CV scoring with detailed rationale",
        )

        # Improvement recommendations task
        improvement_task = Task(
            description="""
            Based on the extracted content and scoring, generate:
            - Top 3-5 specific recommendations to improve the CV
            - Suggestions for restructuring or enhancing weak sections
            - Advice on highlighting key achievements more effectively
            - Potential keywords or skills to add for better ATS compatibility
            """,
            agent=self.improvement_recommendation_agent(),
            expected_output="Actionable CV improvement recommendations",
        )

        # Create crew and kickoff analysis
        crew = Crew(
            agents=[
                self.content_extractor_agent(),
                self.cv_scoring_agent(),
                self.improvement_recommendation_agent(),
            ],
            tasks=[extract_task, scoring_task, improvement_task],
            verbose=2,
        )

        return crew


def extract_cv_text(uploaded_file):
    """Extract text from uploaded CV file."""
    if uploaded_file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        return " ".join([page.extract_text() for page in pdf_reader.pages])
    elif (
        uploaded_file.type
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        doc = docx.Document(uploaded_file)
        return " ".join([para.text for para in doc.paragraphs])
    else:
        raise ValueError("Unsupported file type")


def analyze_cv(uploaded_file):
    """Perform comprehensive CV analysis using CrewAI agents."""
    # Extract text from uploaded file
    cv_text = extract_cv_text(uploaded_file)

    # Initialize agents with CV content
    cv_coach = CVCoachAgents(cv_text)

    # Create and run crew
    crew = cv_coach.create_cv_analysis_crew()
    result = crew.kickoff()

    return result


# Streamlit integration would go here, calling analyze_cv() when needed
