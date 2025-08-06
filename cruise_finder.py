"""Cruise Finder - Modular version of the deep research system."""
import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager

load_dotenv(override=True)

class CruiseResearchManager(ResearchManager):
    """Cruise-specific research manager with specialized prompts."""
    
    async def plan_searches(self, query: str):
        """Override with cruise-specific planning."""
        print("🚢 Planning cruise-specific searches...")
        
        # Temporarily modify the planner's instructions for cruise focus
        original_instructions = self.planner.instructions
        self.planner.instructions = (
            "You are a cruise travel specialist and research planner. Given cruise preferences, "
            "create 5 targeted web searches to find the best cruise options. Focus on: "
            "1. Cruise lines and ships matching preferences "
            "2. Pricing and deals for specific routes "
            "3. Customer reviews and experiences "
            "4. Itinerary details and ports of call "
            "5. Onboard amenities and activities"
        )
        
        result = await super().plan_searches(query)
        self.planner.instructions = original_instructions  # Restore original
        return result
    
    async def search(self, search_item):
        """Override search with cruise-specific instructions."""
        # Temporarily modify searcher instructions
        original_instructions = self.searcher.instructions
        self.searcher.instructions = (
            "You are a cruise search specialist. Search for cruise information and provide "
            "concise summaries focusing on: cruise prices and availability, ship amenities and cabin types, "
            "itinerary highlights, customer review highlights, booking policies. "
            "Keep summaries under 300 words and focus on actionable cruise information."
        )
        
        result = await super().search(search_item)
        self.searcher.instructions = original_instructions  # Restore original
        return result
    
    async def write_report(self, query: str, search_results: list[str]):
        """Override report writing with cruise-specific format."""
        print("📝 Writing cruise comparison report...")
        
        # Temporarily modify writer instructions
        original_instructions = self.writer.instructions
        self.writer.instructions = (
            "You are a cruise travel advisor creating comprehensive cruise recommendations. "
            "Structure your report as a cruise comparison guide with: "
            "- Executive summary of top 3-5 cruise options "
            "- Detailed comparison table (price, duration, destinations, highlights) "
            "- Pros and cons for each option "
            "- Booking recommendations and tips "
            "- Best value assessment "
            "Use markdown formatting with clear sections and comparison tables."
        )
        
        result = await super().write_report(query, search_results)
        self.writer.instructions = original_instructions  # Restore original
        return result

async def run_cruise_research(query: str):
    """Execute cruise-focused research."""
    cruise_manager = CruiseResearchManager()
    async for chunk in cruise_manager.run(query):
        yield chunk

# Create cruise-themed UI
with gr.Blocks(theme=gr.themes.Default(primary_hue="blue")) as ui:
    gr.Markdown("# 🚢 Cruise Finder")
    gr.Markdown("*AI-powered cruise research and recommendation system*")
    gr.Markdown("---")
    
    with gr.Row():
        with gr.Column(scale=4):
            query_input = gr.Textbox(
                label="What kind of cruise are you looking for?",
                placeholder="e.g., 7-day Caribbean cruise under $2000 departing from Miami in March 2024",
                lines=3
            )
        with gr.Column(scale=1):
            search_btn = gr.Button("🔍 Find Cruises", variant="primary", size="lg")
    
    gr.Markdown("### 💡 Example Searches:")
    gr.Markdown("""
    - "Mediterranean cruise in September under $3000"
    - "Alaska cruise with balcony cabin departing from Seattle"  
    - "Caribbean family cruise with kids clubs and water slides"
    - "Luxury cruise to Northern Europe with specialty dining"
    """)
    
    with gr.Row():
        results_output = gr.Markdown(
            label="🎯 Cruise Recommendations",
            value="*Enter your cruise preferences above to start your personalized search...*"
        )
    
    # Connect the interface
    search_btn.click(
        fn=run_cruise_research,
        inputs=query_input,
        outputs=results_output
    )
    
    query_input.submit(
        fn=run_cruise_research,
        inputs=query_input,
        outputs=results_output
    )

if __name__ == "__main__":
    ui.launch(inbrowser=True)