from groq import Groq
import json

class Agent:
    """
    Base class for all agents.
    Every agent has:
      - name: identity
      - role: what it does (system prompt)
      - client: Groq LLM connection
      - memory: conversation history
    """
    def __init__(self, name: str, role: str, model: str = "llama-3.3-70b-versatile"):
        self.name = name
        self.role = role
        self.model = model
        self.memory = []  # stores conversation history
        self.client = Groq()  # reads GROQ_API_KEY from env

    def think(self, user_message: str, tools: list = None) -> str:
        """
        Send a message to this agent and get its response.
        Maintains memory across multiple calls.
        """
        # Add new user message to memory
        self.memory.append({"role": "user", "content": user_message})

        # Build full message list: system prompt + history
        messages = [{"role": "system", "content": self.role}] + self.memory

        # Call Groq API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=2048
        )

        # Extract response text
        reply = response.choices[0].message.content

        # Save agent's reply to memory too
        self.memory.append({"role": "assistant", "content": reply})

        print(f"\n[{self.name}] →\n{reply}\n{'─'*50}")
        return reply

    def reset_memory(self):
        """Clear conversation history between tasks."""
        self.memory = []