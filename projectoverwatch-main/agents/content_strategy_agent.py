from datetime import datetime
from .base_agent import BaseAgent

class ContentStrategyAgent(BaseAgent):
    def __init__(self, api_key: str, model: str):
        super().__init__(api_key, model)

    def create_content_strategy(self, query: str) -> str:
        messages = [{
            "role": "system", 
            "content": """You are a research analyst. Generate ONLY these 10 essential research questions:

            example questions:
1. What are the key facts about this topic?
2. What are the main components or aspects?
3. What are the most recent developments?
4. What are the different perspectives on this topic?
5. What are the common misconceptions?
6. What are the most reliable sources?
7. What are the potential future implications?
8. What are the historical origins?
9. What are the related topics or concepts?
10. What are the most important statistics or data points?

Rules:
- Only provide the questions
- No answers or examples
- No SEO or keyword-related questions
- Keep questions general and research-focused"""
        }, {
            "role": "user",
            "content": f"Generate research questions for: {query}"
        }]

        return self._call_api(messages, stream=True) 