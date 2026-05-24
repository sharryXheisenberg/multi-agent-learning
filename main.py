import os
from dotenv import load_dotenv
from orchestrator import Orchestrator

# Load environment variables from .env file
load_dotenv()

def main():
    # Create the orchestrator (which creates all agents)
    system = Orchestrator()

    # Give it a research task
    topic = "Latest developments in quantum computing 2024"

    # Run the full pipeline
    result = system.run(topic)

    # Save report to file
    with open("report.md", "w") as f:
        f.write(f"# Report: {result['topic']}\n\n")
        f.write(result['report'])

    print("\n Report saved to report.md")
    print("\n Task Log:")
    for entry in result['log']:
        print(f"  {entry['step']} → {entry['agent']}: {entry['status']}")

if __name__ == "__main__":
    main()