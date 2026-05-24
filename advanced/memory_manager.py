import json
from datetime import datetime

class SharedMemory:
    """
    All agents share this memory store.
    Prevents information loss between agent calls.
    Acts as the 'working memory' of the whole system.
    """
    def __init__(self):
        self.store = {}
        self.history = []

    def write(self, agent_name: str, key: str, value: str):
        """Agent writes its output to shared memory."""
        self.store[key] = {
            "value": value,
            "written_by": agent_name,
            "timestamp": datetime.now().isoformat()
        }
        self.history.append(f"{agent_name} wrote '{key}'")

    def read(self, key: str) -> str:
        """Agent reads another agent's output."""
        entry = self.store.get(key)
        return entry["value"] if entry else None

    def get_context_summary(self) -> str:
        """Returns a compact summary of what's in memory."""
        return json.dumps({k: v["written_by"] for k, v in self.store.items()}, indent=2)

    def save_to_file(self, filename: str = "memory_state.json"):
        """Persist memory to disk for inspection."""
        with open(filename, "w") as f:
            json.dump(self.store, f, indent=2)
        print(f"Memory saved to {filename}")