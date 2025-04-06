import requests
import json
from typing import List, Dict
from .report_planner_agent import ReportPlannerAgent
from .content_strategy_agent import ContentStrategyAgent
from .base_agent import BaseAgent
from datetime import datetime

class ReportGeneratorAgent(BaseAgent):
    def __init__(self, api_key: str, model: str):
        super().__init__(api_key, model)
        self.source_urls = {}  # Store source URLs for hyperlinking

    def _call_api(self, messages: list, stream: bool = True, max_tokens: int = 4000) -> str:
        return super()._call_api(messages, stream=True, max_tokens=max_tokens)

    def generate_report(self, structured_data: List[Dict], query: str, strategy: str, current_time: datetime) -> str:
        try:
            self.source_urls = {item['source_id']: item['url'] for item in structured_data}

            messages = [{
                "role": "system", 
                "content": """You are a research analyst. Create a detailed Q&A report with:
                
# Research Report: [Topic]

## Key Questions & Findings
For each key question, provide:
1. The direct answer
2. Supporting evidence from sources
3. Any conflicting information
4. Source citations in [Source X](URL) format

## Sources
{self.format_sources(structured_data)}

Rules:
- Answer each question thoroughly
- Include specific details and evidence
- Highlight conflicting data when present
- Always cite sources
- Maintain academic tone"""
            }, {
                "role": "user",
                "content": f"""Create a detailed Q&A report about "{query}" using this research data:
{json.dumps(structured_data, indent=2)}

Generate answers to these natural questions that would arise about this topic:
1. What are the key facts about this topic?
2. What are the different perspectives or interpretations?
3. What evidence supports each perspective?
4. Are there any controversies or debates?
5. What are the most reliable sources of information?

For each question:
- Provide direct answers with evidence
- Cite sources for all claims
- Include relevant details
- Highlight any contradictions"""
            }]

            report = self._call_api(messages, stream=True, max_tokens=4000)
            return self._ensure_hyperlinks(report)
        except Exception as e:
            print(f"\nError in report generation: {str(e)}")
            return f"Error generating report: {str(e)}"

    def format_sources(self, structured_data: List[Dict]) -> str:
        sources = []
        for item in structured_data:
            sources.append(f"{item['source_id']}. [{item['url']}]({item['url']})")
        return "\n".join(sources)

    def _ensure_hyperlinks(self, report: str) -> str:
        for source_id, url in self.source_urls.items():
            if f"[Source {source_id}]" in report and f"[Source {source_id}]({url})" not in report:
                report = report.replace(
                    f"[Source {source_id}]",
                    f"[Source {source_id}]({url})"
                )
        return report