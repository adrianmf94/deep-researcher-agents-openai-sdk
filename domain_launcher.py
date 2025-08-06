"""Generic domain launcher for the modular research system."""
import gradio as gr
import sys
import importlib
from dotenv import load_dotenv
from research_manager import ResearchManager

load_dotenv(override=True)

def load_domain_config(domain_name: str):
    """Load domain configuration from the domains directory."""
    try:
        config_module = importlib.import_module(f'domains.{domain_name}_config')
        return config_module.DOMAIN_CONFIG
    except ImportError:
        raise ValueError(f"Domain configuration '{domain_name}_config' not found in domains/")

async def run_domain_research(query: str, domain_config: dict):
    """Execute domain-specific research using the configuration."""
    manager = ResearchManager(domain_config=domain_config)
    async for chunk in manager.run(query):
        yield chunk

def create_domain_ui(domain_config: dict):
    """Create a Gradio UI based on domain configuration."""
    ui_config = domain_config['ui']
    
    # Map theme colors to Gradio themes
    theme_map = {
        'blue': gr.themes.Default(primary_hue="blue"),
        'green': gr.themes.Default(primary_hue="green"),
        'orange': gr.themes.Default(primary_hue="orange"),
        'red': gr.themes.Default(primary_hue="red"),
        'purple': gr.themes.Default(primary_hue="purple")
    }
    
    theme = theme_map.get(ui_config['theme_color'], gr.themes.Default())
    
    with gr.Blocks(theme=theme) as ui:
        gr.Markdown(f"# {domain_config['display_name']}")
        gr.Markdown(f"*{domain_config['description']}*")
        gr.Markdown("---")
        
        with gr.Row():
            with gr.Column(scale=4):
                query_input = gr.Textbox(
                    label=ui_config['input_label'],
                    placeholder=ui_config['input_placeholder'],
                    lines=3
                )
            with gr.Column(scale=1):
                search_btn = gr.Button(ui_config['button_text'], variant="primary", size="lg")
        
        if ui_config.get('examples'):
            gr.Markdown("### 💡 Example Searches:")
            examples_text = "\n".join([f"- {example}" for example in ui_config['examples']])
            gr.Markdown(examples_text)
        
        with gr.Row():
            results_output = gr.Markdown(
                label=ui_config['output_label'],
                value=f"*Enter your search criteria above to start your personalized research...*"
            )
        
        # Create a properly wrapped async function for this domain
        async def domain_search_fn(query: str):
            async for chunk in run_domain_research(query, domain_config):
                yield chunk
        
        search_btn.click(
            fn=domain_search_fn,
            inputs=query_input,
            outputs=results_output
        )
        
        query_input.submit(
            fn=domain_search_fn,
            inputs=query_input,
            outputs=results_output
        )
    
    return ui

def main():
    """Main entry point for domain launcher."""
    if len(sys.argv) != 2:
        print("Usage: python domain_launcher.py <domain_name>")
        print("Available domains: cruise, job")
        sys.exit(1)
    
    domain_name = sys.argv[1]
    
    try:
        domain_config = load_domain_config(domain_name)
        ui = create_domain_ui(domain_config)
        print(f"Launching {domain_config['display_name']}...")
        ui.launch(inbrowser=True)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()