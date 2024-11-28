import os
import json
import jsonschema
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import requests

class JSONResumeCV:
    def __init__(self, openai_api_key):
        # JSONResume schema validation
        self.json_schema_url = "https://raw.githubusercontent.com/jsonresume/resume-schema/master/schema.json"
        self.resume_schema = self._fetch_json_schema()
        
        # OpenAI Language Model
        self.llm = ChatOpenAI(
            openai_api_key=openai_api_key, 
            model="gpt-4-turbo",
            temperature=0.3
        )

    def _fetch_json_schema(self):
        """
        Fetch the latest JSONResume schema
        """
        try:
            response = requests.get(self.json_schema_url)
            return response.json()
        except Exception as e:
            print(f"Error fetching schema: {e}")
            return None

    def convert_to_jsonresume(self, input_file):
        """
        Convert various resume formats to JSONResume format
        """
        # Use existing extractors or third-party libraries
        # This is a placeholder - you'd replace with actual conversion logic
        converters = {
            '.pdf': self._pdf_to_jsonresume,
            '.docx': self._docx_to_jsonresume
        }
        
        file_ext = os.path.splitext(input_file)[1].lower()
        converter = converters.get(file_ext)
        
        if not converter:
            raise ValueError("Unsupported file format")
        
        return converter(input_file)

    def _pdf_to_jsonresume(self, pdf_path):
        """
        Convert PDF to JSONResume format
        Placeholder - would use libraries like PyPDF2 or others
        """
        return {
            "basics": {
                "name": "Extracted Name",
                "email": "extracted@email.com"
            },
            "work": [],
            "education": []
        }

    def _docx_to_jsonresume(self, docx_path):
        """
        Convert DOCX to JSONResume format
        Placeholder - would use python-docx or similar
        """
        return {
            "basics": {
                "name": "Extracted Name",
                "email": "extracted@email.com"
            },
            "work": [],
            "education": []
        }

    def validate_jsonresume(self, resume_json):
        """
        Validate resume against JSONResume schema
        """
        try:
            jsonschema.validate(instance=resume_json, schema=self.resume_schema)
            return True
        except jsonschema.exceptions.ValidationError as validation_error:
            print(f"Validation Error: {validation_error}")
            return False

    def create_cv_analysis_crew(self, resume_json):
        """
        Create CrewAI agents for JSONResume analysis
        """
        # JSONResume Specific Agents
        basics_analyst = Agent(
            role='Personal Branding Expert',
            goal='Analyze personal basics and professional summary',
            backstory='A personal branding consultant specializing in professional positioning',
            verbose=True,
            llm=self.llm
        )

        work_experience_analyst = Agent(
            role='Career Development Specialist',
            goal='Evaluate professional experience and achievements',
            backstory='A seasoned recruiter with expertise in talent assessment',
            verbose=True,
            llm=self.llm
        )

        skills_optimizer = Agent(
            role='Skills and Competency Mapper',
            goal='Optimize skills section for maximum marketability',
            backstory='An HR technology expert focused on skills taxonomy',
            verbose=True,
            llm=self.llm
        )

        # Tasks for each section of JSONResume
        basics_task = Task(
            description=f"""Analyze personal basics:
            - Evaluate professional summary
            - Check contact information completeness
            - Assess personal branding statement
            
            Resume Data:
            {json.dumps(resume_json.get('basics', {}), indent=2)}""",
            agent=basics_analyst
        )

        work_task = Task(
            description=f"""Analyze professional experience:
            - Review work history comprehensiveness
            - Evaluate achievement articulation
            - Check for quantifiable outcomes
            
            Work Experience:
            {json.dumps(resume_json.get('work', []), indent=2)}""",
            agent=work_experience_analyst
        )

        skills_task = Task(
            description=f"""Optimize skills section:
            - Assess skills relevance
            - Recommend skill additions/removals
            - Map skills to industry trends
            
            Skills:
            {json.dumps(resume_json.get('skills', []), indent=2)}""",
            agent=skills_optimizer
        )

        # Create Crew
        crew = Crew(
            agents=[basics_analyst, work_experience_analyst, skills_optimizer],
            tasks=[basics_task, work_task, skills_task],
            verbose=2
        )

        return crew

    def review_jsonresume(self, resume_json):
        """
        Comprehensive review of JSONResume
        """
        # Validate resume
        if not self.validate_jsonresume(resume_json):
            raise ValueError("Invalid JSONResume format")

        # Create and run crew
        cv_review_crew = self.create_cv_analysis_crew(resume_json)
        cv_analysis_result = cv_review_crew.kickoff()

        return {
            'full_analysis': cv_analysis_result,
            'sections_scores': self._calculate_section_scores(resume_json)
        }

    def _calculate_section_scores(self, resume_json):
        """
        Calculate scores for different resume sections
        """
        return {
            'basics': self._score_basics(resume_json.get('basics', {})),
            'work': self._score_work_experience(resume_json.get('work', [])),
            'skills': self._score_skills(resume_json.get('skills', [])),
            'education': self._score_education(resume_json.get('education', []))
        }

    def _score_basics(self, basics):
        # Implement scoring logic for personal basics
        return 4  # Out of 5

    def _score_work_experience(self, work_exp):
        # Implement scoring logic for work experience
        return 3  # Out of 5

    def _score_skills(self, skills):
        # Implement scoring logic for skills
        return 4  # Out of 5

    def _score_education(self, education):
        # Implement scoring logic for education
        return 3  # Out of 5

def main():
    # Replace with your actual OpenAI API key
    openai_api_key = 'your-openai-api-key'
    
    cv_reviewer = JSONResumeCV(openai_api_key)
    
    # Example workflow
    try:
        # Convert existing resume
        input_file = 'path/to/your/resume.pdf'
        jsonresume_data = cv_reviewer.convert_to_jsonresume(input_file)
        
        # Review JSONResume
        review_results = cv_reviewer.review_jsonresume(jsonresume_data)
        
        print("JSONResume Analysis Results:")
        print("Full Analysis:", review_results['full_analysis'])
        print("Section Scores:", review_results['sections_scores'])
        
        # Optional: Export enhanced resume
        with open('enhanced_resume.json', 'w') as f:
            json.dump(jsonresume_data, f, indent=2)
    
    except Exception as e:
        print(f"Error in CV review process: {e}")

if __name__ == "__main__":
    main()