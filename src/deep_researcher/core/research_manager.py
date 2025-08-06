from agents import Runner, trace, gen_trace_id
from ..agents.search_agent import search_agent
from ..agents.planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from ..agents.writer_agent import writer_agent, ReportData
from ..agents.email_agent import email_agent
import asyncio

class ResearchManager:
    """Modular research manager that can be configured for different domains."""
    
    def __init__(self, domain_config=None):
        """Initialize with optional domain configuration."""
        self.domain_config = domain_config

    async def run(self, query: str):
        """ Run the deep research process, yielding the status updates and the final report"""
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            print("Starting research...")
            search_plan = await self.plan_searches(query)
            yield "Searches planned, starting to search..."     
            search_results = await self.perform_searches(search_plan)
            yield "Searches complete, writing report..."
            report = await self.write_report(query, search_results)
            yield "Report written, sending email..."
            await self.send_email(report)
            yield "Email sent, research complete"
            yield report.markdown_report
        

    async def plan_searches(self, query: str) -> WebSearchPlan:
        """ Plan the searches to perform for the query """
        print("Planning searches...")
        
        # Apply domain-specific instructions if configured
        original_instructions = planner_agent.instructions
        if self.domain_config and 'agent_instructions' in self.domain_config:
            planner_agent.instructions = self.domain_config['agent_instructions'].get('planner', original_instructions)
        
        try:
            result = await Runner.run(
                planner_agent,
                f"Query: {query}",
            )
            print(f"Will perform {len(result.final_output.searches)} searches")
            return result.final_output_as(WebSearchPlan)
        finally:
            # Always restore original instructions
            planner_agent.instructions = original_instructions

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """ Perform the searches to perform for the query """
        print("Searching...")
        num_completed = 0
        tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]
        results = []
        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
            num_completed += 1
            print(f"Searching... {num_completed}/{len(tasks)} completed")
        print("Finished searching")
        return results

    async def search(self, item: WebSearchItem) -> str | None:
        """ Perform a search for the query """
        input = f"Search term: {item.query}\nReason for searching: {item.reason}"
        
        # Apply domain-specific instructions if configured
        original_instructions = search_agent.instructions
        if self.domain_config and 'agent_instructions' in self.domain_config:
            search_agent.instructions = self.domain_config['agent_instructions'].get('searcher', original_instructions)
        
        try:
            result = await Runner.run(
                search_agent,
                input,
            )
            return str(result.final_output)
        except Exception:
            return None
        finally:
            # Always restore original instructions
            search_agent.instructions = original_instructions

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """ Write the report for the query """
        print("Thinking about report...")
        input = f"Original query: {query}\nSummarized search results: {search_results}"
        
        # Apply domain-specific instructions if configured
        original_instructions = writer_agent.instructions
        if self.domain_config and 'agent_instructions' in self.domain_config:
            writer_agent.instructions = self.domain_config['agent_instructions'].get('writer', original_instructions)
        
        try:
            result = await Runner.run(
                writer_agent,
                input,
            )
            print("Finished writing report")
            return result.final_output_as(ReportData)
        finally:
            # Always restore original instructions
            writer_agent.instructions = original_instructions
    
    async def send_email(self, report: ReportData) -> None:
        print("Writing email...")
        result = await Runner.run(
            email_agent,
            report.markdown_report,
        )
        print("Email sent")
        return report