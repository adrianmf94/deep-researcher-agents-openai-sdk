"""Job Finder - Uses the modular domain launcher."""
import sys
from pathlib import Path

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from deep_researcher.core import load_domain_config, create_domain_ui

if __name__ == "__main__":
    # Load job domain configuration and launch
    domain_config = load_domain_config('job')
    ui = create_domain_ui(domain_config)
    print(f"Launching {domain_config['display_name']}...")
    ui.launch(inbrowser=True)