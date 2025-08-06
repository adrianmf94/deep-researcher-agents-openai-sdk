# 🎯 Modular AI Research Framework

A flexible, domain-specific AI research system built with OpenAI Agents SDK and Gradio. Easily create specialized research assistants for any industry or use case.

## 🚀 Features

- **Modular Architecture**: One codebase, multiple research domains
- **Easy Customization**: Override prompts to create new research types
- **Beautiful UI**: Gradio-powered interfaces with domain-specific themes
- **Async Workflow**: Multi-agent research pipeline with real-time updates
- **Email Integration**: Automatic report delivery via SendGrid

## 🏗️ Architecture

The system uses a base `ResearchManager` that can be specialized for different domains by overriding agent instructions:

```python
class CruiseResearchManager(ResearchManager):
    async def plan_searches(self, query: str):
        # Override planner with cruise-specific instructions
        original_instructions = self.planner.instructions
        self.planner.instructions = "You are a cruise travel specialist..."
        result = await super().plan_searches(query)
        self.planner.instructions = original_instructions
        return result
```

## 📁 Project Structure

```
deep_researcher_openai_sdk/
├── research_manager.py      # Base research orchestrator
├── planner_agent.py         # Search planning agent
├── search_agent.py          # Web search agent  
├── writer_agent.py          # Report writing agent
├── email_agent.py           # Email delivery agent
├── cruise_finder.py         # 🚢 Cruise research domain
├── job_finder.py            # 💼 Job market research domain
├── demo_launcher.py         # Multi-domain demo interface
└── deep_research.py         # Original general research
```

## 🎯 Available Research Domains

### 🚢 Cruise Finder
Specialized for cruise research with focus on:
- Cruise lines and ship amenities
- Pricing and deals analysis
- Itinerary and destination insights
- Customer reviews and experiences

### 💼 Job Market Analyzer  
Optimized for career research including:
- Job availability and requirements
- Salary ranges and compensation
- Skills and qualifications analysis
- Company insights and culture

### 🔍 General Research
The original flexible research assistant for any topic.

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- UV package manager
- OpenAI API key
- SendGrid API key (optional, for email features)

### Installation

```bash
# Clone and setup
git clone <your-repo>
cd deep_researcher_openai_sdk

# Install dependencies with UV
uv sync

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Environment Variables

Create a `.env` file with:

```bash
OPENAI_API_KEY=your_openai_api_key
OPENAI_MEDIUM_MODEL=gpt-4o-mini
SENDGRID_API_KEY=your_sendgrid_key  # Optional
FROM_EMAIL=your@email.com           # Optional  
TO_EMAIL=recipient@email.com        # Optional
```

### Running the Applications

```bash
# Launch cruise finder
uv run python cruise_finder.py

# Launch job market analyzer  
uv run python job_finder.py

# Launch multi-domain demo
uv run python demo_launcher.py

# Launch original general research
uv run python deep_research.py
```

## 🛠️ Creating New Research Domains

Creating a new research domain is simple - just override the agent instructions:

```python
class PropertyResearchManager(ResearchManager):
    """Real estate research manager."""
    
    async def plan_searches(self, query: str):
        original_instructions = self.planner.instructions
        self.planner.instructions = (
            "You are a real estate analyst. Create searches focusing on: "
            "property listings, market trends, neighborhood analysis, "
            "pricing data, and investment opportunities."
        )
        result = await super().plan_searches(query)
        self.planner.instructions = original_instructions
        return result
```

Then create a UI file:

```python
# property_finder.py
async def run_property_research(query: str):
    manager = PropertyResearchManager()
    async for chunk in manager.run(query):
        yield chunk

with gr.Blocks(theme=gr.themes.Default(primary_hue="orange")) as ui:
    gr.Markdown("# 🏠 Property Research Assistant")
    # ... rest of UI setup
```

## 🎨 Customization Options

### Agent Customization
- **Planner Agent**: Override `plan_searches()` for domain-specific search strategies
- **Search Agent**: Override `search()` for specialized information extraction
- **Writer Agent**: Override `write_report()` for custom report formats
- **Email Agent**: Customize email templates and formatting

### UI Customization
- **Themes**: Change Gradio theme colors for each domain
- **Layouts**: Customize interface layouts and components
- **Examples**: Add domain-specific example queries
- **Branding**: Update titles, descriptions, and emojis

## 📊 Example Research Queries

### 🚢 Cruise Research
- "7-day Mediterranean cruise under $3000 in September"
- "Family-friendly Caribbean cruise with kids activities"
- "Luxury Northern Europe cruise with specialty dining"

### 💼 Job Market Research
- "Remote software engineer jobs with $120k+ salary"
- "Data scientist career prospects in healthcare"
- "Entry-level marketing positions in Austin, Texas"

## 🔧 Technical Details

### Multi-Agent Workflow
1. **Planning**: Generate targeted search queries
2. **Searching**: Perform concurrent web searches
3. **Analysis**: Synthesize results into comprehensive reports
4. **Delivery**: Email formatted reports (optional)

### Key Technologies
- **OpenAI Agents SDK**: Core AI agent framework
- **Gradio**: Web interface and real-time updates
- **Pydantic**: Data validation and type safety
- **SendGrid**: Email delivery integration
- **Python Asyncio**: Concurrent processing

## 🤝 Contributing

1. Fork the repository
2. Create a new research domain
3. Test your implementation
4. Submit a pull request

## 📄 License

MIT License - feel free to use this for your own projects!

## 🌟 Portfolio Value

This project demonstrates:
- **System Architecture**: Clean, modular design patterns
- **AI Integration**: Advanced multi-agent workflows
- **UI/UX Design**: Domain-specific user experiences  
- **Code Reusability**: One framework, multiple applications
- **Business Value**: Real-world problem solving

Perfect for showcasing full-stack AI development skills! 🚀