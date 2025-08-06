"""Cruise domain configuration for the modular research system."""

DOMAIN_CONFIG = {
    "name": "cruise",
    "display_name": "🚢 Cruise Finder",
    "description": "AI-powered cruise research and recommendation system",
    
    "ui": {
        "theme_color": "blue",
        "input_label": "What kind of cruise are you looking for?",
        "input_placeholder": "e.g., 7-day Caribbean cruise under $2000 departing from Miami in March 2024",
        "button_text": "🔍 Find Cruises",
        "output_label": "🎯 Cruise Recommendations",
        "examples": [
            "Mediterranean cruise in September under $3000",
            "Alaska cruise with balcony cabin departing from Seattle",
            "Caribbean family cruise with kids clubs and water slides", 
            "Luxury cruise to Northern Europe with specialty dining"
        ]
    },
    
    "agent_instructions": {
        "planner": (
            "You are a cruise travel specialist and research planner. Given cruise preferences, "
            "create 5 targeted web searches to find the best cruise options. Focus on: "
            "1. Cruise lines and ships matching preferences "
            "2. Pricing and deals for specific routes "
            "3. Customer reviews and experiences "
            "4. Itinerary details and ports of call "
            "5. Onboard amenities and activities"
        ),
        
        "searcher": (
            "You are a cruise search specialist. Search for cruise information and provide "
            "concise summaries focusing on: cruise prices and availability, ship amenities and cabin types, "
            "itinerary highlights, customer review highlights, booking policies. "
            "Keep summaries under 300 words and focus on actionable cruise information."
        ),
        
        "writer": (
            "You are a cruise travel advisor creating comprehensive cruise recommendations. "
            "Structure your report as a cruise comparison guide with: "
            "- Executive summary of top 3-5 cruise options "
            "- Detailed comparison table (price, duration, destinations, highlights) "
            "- Pros and cons for each option "
            "- Booking recommendations and tips "
            "- Best value assessment "
            "Use markdown formatting with clear sections and comparison tables."
        )
    }
}