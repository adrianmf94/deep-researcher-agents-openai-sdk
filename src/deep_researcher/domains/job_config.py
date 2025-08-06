"""Job market domain configuration for the modular research system."""

DOMAIN_CONFIG = {
    "name": "job",
    "display_name": "💼 Job Market Analyzer",
    "description": "AI-powered job market research and career guidance",
    
    "ui": {
        "theme_color": "green",
        "input_label": "What job market information are you looking for?",
        "input_placeholder": "e.g., Software Engineer jobs in San Francisco with $120k+ salary",
        "button_text": "🔍 Analyze Job Market",
        "output_label": "📈 Job Market Analysis",
        "examples": [
            "Data Scientist remote jobs with machine learning focus",
            "Entry level marketing jobs in Austin Texas",
            "Senior Python developer salary trends 2024",
            "Product Manager career path at tech startups"
        ]
    },
    
    "agent_instructions": {
        "planner": (
            "You are a career research specialist. Given a job search query, "
            "create 5 targeted searches to find comprehensive job market information. Focus on: "
            "1. Current job openings and requirements "
            "2. Salary ranges and compensation data "
            "3. Skills and qualifications in demand "
            "4. Company insights and culture "
            "5. Career growth and industry trends"
        ),
        
        "searcher": (
            "You are a job market analyst. Search for employment information and provide "
            "concise summaries focusing on: job availability, salary ranges, required skills, "
            "company information, remote work options, growth prospects. "
            "Keep summaries under 300 words and focus on actionable career insights."
        ),
        
        "writer": (
            "You are a career advisor creating comprehensive job market reports. "
            "Structure your report with: "
            "- Executive summary of job market conditions "
            "- Salary analysis and compensation ranges "
            "- Key skills and qualifications needed "
            "- Top companies and opportunities "
            "- Career development recommendations "
            "- Job search strategy tips "
            "Use markdown formatting with clear sections and data tables."
        )
    }
}