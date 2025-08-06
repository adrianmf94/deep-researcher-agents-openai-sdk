"""Job Finder - Uses the modular domain launcher."""
from domain_launcher import load_domain_config, create_domain_ui

if __name__ == "__main__":
    # Load job domain configuration and launch
    domain_config = load_domain_config('job')
    ui = create_domain_ui(domain_config)
    print(f"Launching {domain_config['display_name']}...")
    ui.launch(inbrowser=True)