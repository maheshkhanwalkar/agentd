import copy
import datetime
import os
import sys

from deepagents import create_deep_agent
from deepagents.backends import LocalShellBackend

SYSTEM_PROMPT = """
You are an agentic coding assistant. For a user's exploratory questions, be conversational and ask questions
to dig further. Otherwise, focus on execution.
"""

class ManagedAgent:
    def __init__(self, model_name: str):
        full_prompt = SYSTEM_PROMPT + self._inject_system_context()

        self.agent = create_deep_agent(model_name,
           system_prompt=full_prompt,
           backend=LocalShellBackend(os.getcwd(), virtual_mode=False)
        )
        self.messages_memory = {
            "messages": []
        }

    def invoke(self, message: str) -> str:
        self._append_message(message, 'user')
        result = self.agent.invoke(copy.deepcopy(self.messages_memory))

        ai_response = result['messages'][-1].content
        self._append_message(ai_response, "assistant")

        return ai_response

    def _append_message(self, message: str, actor: str):
        self.messages_memory["messages"].append({
            "role": actor,
            "content": message,
        })

    @staticmethod
    def _inject_system_context() -> str:
        cwd = os.getcwd()
        os_platform = sys.platform
        curr_time = datetime.datetime.now().strftime("%Y%m%d")

        return (f"\nThe user's current directory is {cwd}. The OS is {os_platform}. "
                f"The current date is {curr_time}.")
