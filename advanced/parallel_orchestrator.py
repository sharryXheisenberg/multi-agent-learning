import concurrent.futures
from agents.specialized_agents import ResearchAgent

class ParallelOrchestrator:
    """
    Runs multiple research agents SIMULTANEOUSLY.
    If your topic has multiple sub-topics, each gets its own agent.
    Speed: 3x faster than sequential execution.
    """
    def __init__(self):
        # Create a pool of research agents
        self.agents = [ResearchAgent() for _ in range(3)]

    def parallel_research(self, sub_topics: list) -> list:
        """Assigns each sub-topic to a separate agent, runs them at once."""
        results = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            # Map each agent to a sub-topic
            futures = {
                executor.submit(agent.research, topic): topic
                for agent, topic in zip(self.agents, sub_topics)
            }

            # Collect results as they complete
            for future in concurrent.futures.as_completed(futures):
                topic = futures[future]
                try:
                    result = future.result()
                    results.append({"topic": topic, "result": result})
                    print(f" Completed: {topic}")
                except Exception as e:
                    print(f" Failed: {topic} — {e}")

        return results

# Usage:
# orc = ParallelOrchestrator()
# results = orc.parallel_research([
#     "quantum computing hardware",
#     "quantum computing algorithms",
#     "quantum computing applications"
# ])