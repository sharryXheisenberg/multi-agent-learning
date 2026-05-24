from agents.specialized_agents import ResearchAgent, AnalystAgent, WriterAgent

class Orchestrator:
    """
    The Orchestrator coordinates all agents.
    
    It decides:
      - Which agents to call
      - In what order
      - What information to pass between them
    
    This is the BRAIN of the multi-agent system.
    """
    def __init__(self):
        # Initialize all specialist agents
        self.researcher = ResearchAgent()
        self.analyst    = AnalystAgent()
        self.writer     = WriterAgent()
        self.task_log   = []  # audit trail of what happened

    def log(self, step: str, agent: str, status: str):
        entry = {"step": step, "agent": agent, "status": status}
        self.task_log.append(entry)
        print(f"[Orchestrator] Step '{step}' → {agent}: {status}")

    def run(self, topic: str) -> dict:
        """
        Main pipeline. Runs all agents in sequence.
        Returns: dict with research, analysis, report, and log.
        """
        print(f"\n{'='*60}")
        print(f"ORCHESTRATOR STARTING TASK: '{topic}'")
        print(f"{'='*60}\n")

        # ── Phase 1: Research ──────────────────────────────────────
        self.log("research", "ResearchAgent", "starting")
        research_output = self.researcher.research(topic)
        self.log("research", "ResearchAgent", "complete")

        # ── Phase 2: Analysis ──────────────────────────────────────
        self.log("analysis", "AnalystAgent", "starting")
        analysis_output = self.analyst.analyze(research_output, topic)
        self.log("analysis", "AnalystAgent", "complete")

        # ── Phase 3: Writing ───────────────────────────────────────
        self.log("writing", "WriterAgent", "starting")
        final_report = self.writer.write_report(
            research_output, analysis_output, topic
        )
        self.log("writing", "WriterAgent", "complete")

        print(f"\n{'='*60}")
        print("TASK COMPLETE — FINAL REPORT READY")
        print(f"{'='*60}\n")

        return {
            "topic": topic,
            "research": research_output,
            "analysis": analysis_output,
            "report": final_report,
            "log": self.task_log
        }