"""Job Finder - Another example of the modular research system."""
import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager

load_dotenv(override=True)

class JobResearchManager(ResearchManager):
    """Job market research manager with specialized prompts."""
    
    async def plan_searches(self, query: str):
        """Override with job market planning."""
        print("💼 Planning job market searches...")
        
        original_instructions = self.planner.instructions
        self.planner.instructions = (
            "You are a career research specialist. Given a job search query, "
            "create 5 targeted searches to find comprehensive job market information. Focus on: "
            "1. Current job openings and requirements "
            "2. Salary ranges and compensation data "
            "3. Skills and qualifications in demand "
            "4. Company insights and culture "
            "5. Career growth and industry trends"
        )
        
        result = await super().plan_searches(query)
        self.planner.instructions = original_instructions
        return result
    
    async def search(self, search_item):
        """Override search with job-specific instructions."""
        original_instructions = self.searcher.instructions
        self.searcher.instructions = (
            "You are a job market analyst. Search for employment information and provide "
            "concise summaries focusing on: job availability, salary ranges, required skills, "
            "company information, remote work options, growth prospects. "
            "Keep summaries under 300 words and focus on actionable career insights."
        )
        
        result = await super().search(search_item)
        self.searcher.instructions = original_instructions
        return result
    
    async def write_report(self, query: str, search_results: list[str]):
        """Override report writing with job market format."""
        print("📊 Writing job market analysis...")
        
        original_instructions = self.writer.instructions
        self.writer.instructions = (
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
        
        result = await super().write_report(query, search_results)
        self.writer.instructions = original_instructions
        return result

async def run_job_research(query: str):
    """Execute job market research."""
    job_manager = JobResearchManager()
    async for chunk in job_manager.run(query):
        yield chunk

# Create job-themed UI
with gr.Blocks(theme=gr.themes.Default(primary_hue="green")) as ui:
    gr.Markdown("# 💼 Job Market Analyzer")
    gr.Markdown("*AI-powered job market research and career guidance*")
    gr.Markdown("---")
    
    with gr.Row():
        with gr.Column(scale=4):
            query_input = gr.Textbox(
                label="What job market information are you looking for?",
                placeholder="e.g., Software Engineer jobs in San Francisco with $120k+ salary",
                lines=3
            )
        with gr.Column(scale=1):
            search_btn = gr.Button("🔍 Analyze Job Market", variant="primary", size="lg")
    
    gr.Markdown("### 💡 Example Searches:")
    gr.Markdown("""
    - "Data Scientist remote jobs with machine learning focus"
    - "Entry level marketing jobs in Austin Texas"  
    - "Senior Python developer salary trends 2024"
    - "Product Manager career path at tech startups"
    """)
    
    with gr.Row():
        results_output = gr.Markdown(
            label="📈 Job Market Analysis",
            value="*Enter your job search criteria above to start your market analysis...*"
        )
    
    # Connect the interface
    search_btn.click(
        fn=run_job_research,
        inputs=query_input,
        outputs=results_output
    )
    
    query_input.submit(
        fn=run_job_research,
        inputs=query_input,
        outputs=results_output
    )

if __name__ == "__main__":
    ui.launch(inbrowser=True)