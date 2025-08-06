"""Demo Launcher - Shows multiple research domains in one interface."""
import gradio as gr
from dotenv import load_dotenv
import sys
from pathlib import Path

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from deep_researcher.core import ResearchManager, load_domain_config

load_dotenv(override=True)

# Load domain configurations
cruise_config = load_domain_config('cruise')
job_config = load_domain_config('job')

async def run_research(query: str, domain: str):
    """Run research based on selected domain."""
    if domain == "Cruises 🚢":
        manager = ResearchManager(domain_config=cruise_config)
        prefix = "🚢 Searching for cruise options..."
    elif domain == "Jobs 💼":
        manager = ResearchManager(domain_config=job_config)
        prefix = "💼 Analyzing job market..."
    else:  # General
        manager = ResearchManager()  # No domain config = general research
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