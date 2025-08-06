# 🎯 Modular AI Research Framework

## The Problem I Solved

**The Challenge:** Building AI research assistants for different industries (cruises, jobs, real estate) typically requires writing separate applications from scratch. Each domain needs specialized prompts, different UI themes, and unique workflows - leading to code duplication and maintenance nightmares.

**My Solution:** Created a configuration-driven architecture where new research domains can be added with **zero code changes** - just configuration files. One codebase powers unlimited specialized research assistants.

**The Impact:** Reduced new domain creation from days of development to 5 minutes of configuration. Eliminated 200+ lines of duplicated code per domain down to just 9 lines.

---

## What This Framework Does

This is an AI-powered research system that automatically:
1. **Plans** targeted searches based on your query
2. **Searches** the web concurrently for relevant information  
3. **Analyzes** results and writes comprehensive reports
4. **Delivers** formatted reports via email (optional)

**Current Domains:**
- 🚢 **Cruise Finder** - Find the perfect cruise with pricing, itineraries, and reviews
- 💼 **Job Market Analyzer** - Research career opportunities, salaries, and companies

---

## How The Technical Solution Works

### The Architecture Problem
Originally, each research domain required its own class with hardcoded logic:

```python
# ❌ Old Way: Hardcoded, non-reusable
class CruiseResearchManager(ResearchManager):
    async def plan_searches(self, query: str):
        # 50+ lines of cruise-specific code
        self.planner.instructions = "Cruise specialist prompts..."
```

### The Modular Solution
Now, domains are pure configuration files that get injected at runtime:

```python
# ✅ New Way: Configuration-driven, infinitely extensible
DOMAIN_CONFIG = {
    "name": "cruise",
    "agent_instructions": {
        "planner": "You are a cruise travel specialist...",
        "searcher": "Focus on cruise prices and amenities...", 
        "writer": "Structure as cruise comparison guide..."
    },
    "ui": {
        "theme_color": "blue",
        "title": "🚢 Cruise Finder"
    }
}
```

### Multi-Agent Architecture Deep Dive

#### Core Agent Framework (OpenAI Agents SDK)
Built on OpenAI's latest Agents SDK, the system implements several key **agentic design patterns**:

**1. Agent Workflows** - Orchestrated sequences of AI operations
```python
# Each agent has specialized instructions and capabilities
planner_agent = Agent(
    name="PlannerAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=WebSearchPlan,  # Structured outputs via Pydantic
)
```

**2. Tool Integration** - Agents can call functions and APIs
```python
@function_tool
def search_web(query: str) -> str:
    # OpenAI WebSearchTool integration
    # Converts regular functions into agent-callable tools
```

**3. Agent Collaboration** - Agents working together via handoffs
```python
# Agent A completes work, hands off to Agent B
handoffs = [emailer_agent]
```

#### The 4-Agent Research Pipeline

**1. Planner Agent** - Strategic query decomposition
- Uses **Structured Outputs** (Pydantic models) for consistent planning
- Breaks complex queries into targeted search strategies
- Applies domain-specific planning logic via injected instructions

**2. Search Agent** - Concurrent information gathering
- Leverages OpenAI's hosted **WebSearchTool** for real-time web search
- Implements **ModelSettings** with `tool_choice="required"`
- Performs searches in parallel using asyncio for speed

**3. Writer Agent** - Intelligent synthesis
- Uses **structured outputs** to ensure consistent report format
- Generates comprehensive markdown reports (1000+ words)
- Includes follow-up questions for iterative research

**4. Email Agent** - Automated delivery
- Converts markdown to HTML with professional formatting
- Integrates with SendGrid API for reliable email delivery
- Handles subject line generation and template application

#### Advanced Technical Features

**Runtime Instruction Injection:**
```python
# Domain-specific instructions applied at runtime
original_instructions = planner_agent.instructions
if self.domain_config:
    planner_agent.instructions = domain_config['agent_instructions']['planner']
# Execute with specialized knowledge
result = await Runner.run(planner_agent, query)
# Restore original instructions for next use
planner_agent.instructions = original_instructions
```

**Concurrent Processing:**
```python
# Multiple agents working simultaneously
tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]
results = await asyncio.gather(*tasks)
```

**Distributed Tracing:**
```python
# Full observability across agent interactions
with trace("Research trace", trace_id=trace_id):
    # All agent calls tracked at https://platform.openai.com/traces
```

This architecture enables the same codebase to become a cruise expert, job market analyst, or any other specialist by simply changing the configuration - no code modifications required.

---

## Running This Project Locally

### Prerequisites
- Python 3.12+ installed
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))
- UV package manager: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Setup (2 minutes)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/deep_researcher_openai_sdk
cd deep_researcher_openai_sdk

# 2. Install dependencies
uv sync

# 3. Configure environment
cp .env.example .env
# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=your_actual_api_key_here
```

### Launch Applications

```bash
# Method 1: Launch specific domains
uv run python cruise_finder.py      # 🚢 Cruise research
uv run python job_finder.py         # 💼 Job market analysis

# Method 2: Generic launcher (recommended)  
uv run python domain_launcher.py cruise
uv run python domain_launcher.py job

# Method 3: Original general research
uv run python deep_research.py      # 🔍 Any topic research
```

The web interface will open automatically at `http://localhost:7860`

### Adding New Domains (5 minutes)

Create a new research domain without any code changes:

```bash
# 1. Copy existing config
cp domains/cruise_config.py domains/travel_config.py

# 2. Edit the prompts in travel_config.py for your domain

# 3. Launch immediately
uv run python domain_launcher.py travel
```

---

## Example Queries You Can Try

**🚢 Cruise Research:**
- "7-day Mediterranean cruise under $3000 in September"
- "Family-friendly Caribbean cruise with kids activities"
- "Alaska cruise with balcony cabin departing from Seattle"

**💼 Job Market Research:**  
- "Remote software engineer jobs with $120k+ salary"
- "Data scientist career prospects in healthcare" 
- "Entry-level marketing positions in Austin, Texas"

---

## Project Structure

```
deep_researcher_openai_sdk/
├── domains/
│   ├── cruise_config.py     # 🚢 Cruise domain configuration
│   └── job_config.py        # 💼 Job market configuration
├── domain_launcher.py       # Generic UI generator
├── research_manager.py      # Core orchestration logic
├── *_agent.py              # Specialized AI agents
├── cruise_finder.py        # Domain launcher (9 lines)
└── job_finder.py           # Domain launcher (9 lines)
```

The beauty is in the simplicity - each domain file is now just 9 lines that load a configuration.

---

## Acknowledgments

This project was inspired by and built upon concepts from **Ed Donner's** excellent course ["The Complete Agentic AI Engineering Course (2025)"](https://www.udemy.com/course/agentic-ai-engineering/) on Udemy. His teaching on multi-agent systems and the OpenAI Agents SDK provided the foundational knowledge that made this modular architecture possible.

The original course project focused on general research capabilities. I extended it to solve the domain specialization problem through configuration-driven architecture, making it infinitely extensible for different industries and use cases.

---

## Why This Matters

This project demonstrates several key engineering principles:

- **Problem-Solving**: Identified code duplication pain point and solved it systematically
- **System Design**: Built for extensibility and maintainability from day one
- **Technical Leadership**: Chose architecture that scales with business needs
- **Real-World Impact**: Reduced development time from days to minutes

Perfect for showcasing how senior engineers think about building maintainable, scalable systems that solve actual business problems.

---

## License

MIT License - Use this framework for your own specialized research assistants!