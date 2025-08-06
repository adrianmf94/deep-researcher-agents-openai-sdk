"""Demo Launcher - Shows multiple research domains in one interface."""
import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager

load_dotenv(override=True)

# Import our specialized managers
import sys
sys.path.append('.')

class CruiseResearchManager(ResearchManager):
    """Cruise-specific research manager."""
    
    async def plan_searches(self, query: str):
        original_instructions = self.planner.instructions
        self.planner.instructions = (
            "You are a cruise travel specialist. Create 5 targeted searches for cruise options focusing on: "
            "cruise lines, pricing, itineraries, reviews, and ship amenities."
        )
        result = await super().plan_searches(query)
        self.planner.instructions = original_instructions
        return result

class JobResearchManager(ResearchManager):
    """Job market research manager."""
    
    async def plan_searches(self, query: str):
        original_instructions = self.planner.instructions
        self.planner.instructions = (
            "You are a career research specialist. Create 5 targeted searches for job market analysis focusing on: "
            "job openings, salary ranges, required skills, company insights, and industry trends."
        )
        result = await super().plan_searches(query)
        self.planner.instructions = original_instructions
        return result

class GeneralResearchManager(ResearchManager):
    """General research manager (original)."""
    pass

async def run_research(query: str, domain: str):
    """Run research based on selected domain."""
    if domain == "Cruises 🚢":
        manager = CruiseResearchManager()
        prefix = "🚢 Searching for cruise options..."
    elif domain == "Jobs 💼":
        manager = JobResearchManager()
        prefix = "💼 Analyzing job market..."
    else:  # General
        manager = GeneralResearchManager()
        prefix = "🔍 Conducting general research..."
    
    yield prefix
    async for chunk in manager.run(query):
        yield chunk

# Create multi-domain UI
with gr.Blocks(theme=gr.themes.Default(primary_hue="purple")) as ui:
    gr.Markdown("# 🎯 Modular Research Assistant")
    gr.Markdown("*One codebase, multiple specialized research domains*")
    gr.Markdown("---")
    
    with gr.Row():
        with gr.Column(scale=2):
            domain_selector = gr.Radio(
                choices=["General 🔍", "Cruises 🚢", "Jobs 💼"],
                label="Choose Research Domain",
                value="General 🔍"
            )
        with gr.Column(scale=4):
            query_input = gr.Textbox(
                label="What would you like to research?",
                placeholder="Enter your research query...",
                lines=2
            )
        with gr.Column(scale=1):
            search_btn = gr.Button("🚀 Research", variant="primary", size="lg")
    
    gr.Markdown("### 💡 Example Queries by Domain:")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("**🔍 General Research:**")
            gr.Markdown("- Climate change impact on agriculture")
            gr.Markdown("- Latest AI breakthroughs 2024")
        with gr.Column():
            gr.Markdown("**🚢 Cruise Research:**") 
            gr.Markdown("- Mediterranean cruise in September")
            gr.Markdown("- Family-friendly Caribbean cruises")
        with gr.Column():
            gr.Markdown("**💼 Job Research:**")
            gr.Markdown("- Remote software engineer jobs")
            gr.Markdown("- Data scientist salary trends")
    
    with gr.Row():
        results_output = gr.Markdown(
            label="📊 Research Results",
            value="*Select a domain and enter your query to start researching...*"
        )
    
    # Connect the interface
    def launch_research(query, domain):
        return run_research(query, domain)
    
    search_btn.click(
        fn=launch_research,
        inputs=[query_input, domain_selector],
        outputs=results_output
    )
    
    query_input.submit(
        fn=launch_research,
        inputs=[query_input, domain_selector],
        outputs=results_output
    )

if __name__ == "__main__":
    print("🎯 Launching Modular Research Assistant...")
    print("Available domains: General, Cruises, Jobs")
    ui.launch(inbrowser=True)