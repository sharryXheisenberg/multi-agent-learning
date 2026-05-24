from agents.base_agent import Agent
from duckduckgo_search import DDGS

class ResearchAgent(Agent):
    """
    Searches the web using DuckDuckGo (no API key needed).
    Returns structured results.
    """
    def __init__(self):
        super().__init__(
            name="Researcher",
            role="""You are a research specialist. When given a topic:
1. Identify 3-5 key sub-questions to answer.
2. Given search results, extract the most relevant facts.
3. Always cite sources (URLs).
4. Output as structured bullet points.
Be concise and factual."""
        )
        self.search_engine = DDGS()

    def search_web(self, query: str, max_results: int = 5) -> str:
        """Performs real web search via DuckDuckGo."""
        print(f"[Researcher] Searching: '{query}'")
        results = list(self.search_engine.text(query, max_results=max_results))

        if not results:
            return "No results found."

        # Format results for the LLM
        formatted = ""
        for i, r in enumerate(results, 1):
            formatted += f"\n[{i}] Title: {r['title']}\n"
            formatted += f"    URL: {r['href']}\n"
            formatted += f"    Summary: {r['body']}\n"
        return formatted

    def research(self, topic: str) -> str:
        """Main method: search + analyze with LLM."""
        # Step 1: search the web
        raw_results = self.search_web(topic)

        # Step 2: ask LLM to extract and structure findings
        prompt = f"""Topic to research: "{topic}"

Here are web search results:
{raw_results}

Extract and structure the most important facts about this topic.
Include source URLs."""
        return self.think(prompt)


class AnalystAgent(Agent):
    """
    Reasons over research findings.
    Identifies patterns, gaps, and key insights.
    """
    def __init__(self):
        super().__init__(
            name="Analyst",
            role="""You are a critical thinking analyst. Given research findings:
1. Identify the 3 most important insights.
2. Note any contradictions or knowledge gaps.
3. Assess the reliability of information.
4. Suggest what additional research might be needed.
5. Output structured analysis with clear sections.
Be analytical and objective."""
        )

    def analyze(self, research_data: str, original_topic: str) -> str:
        """Analyzes research output and produces structured insights."""
        prompt = f"""Original research topic: "{original_topic}"

Research findings to analyze:
{research_data}

Provide a critical analysis with:
- Key Insights (top 3)
- Information Quality Assessment
- Knowledge Gaps
- Confidence Level (High/Medium/Low)"""
        return self.think(prompt)


class WriterAgent(Agent):
    """
    Takes research + analysis and writes a polished final report.
    """
    def __init__(self):
        super().__init__(
            name="Writer",
            role="""You are a professional report writer. Given research and analysis:
1. Write a clear, well-structured report.
2. Use this format:
   - Executive Summary (2-3 sentences)
   - Key Findings (bullet points)
   - Detailed Analysis (paragraphs)
   - Conclusion
   - Sources
3. Write for a general audience.
4. Be informative but concise."""
        )

    def write_report(self, research: str, analysis: str, topic: str) -> str:
        """Combines research + analysis into a final report."""
        prompt = f"""Write a comprehensive report on: "{topic}"

RESEARCH DATA:
{research}

ANALYST INSIGHTS:
{analysis}

Produce a polished, structured report following your instructions."""
        return self.think(prompt)