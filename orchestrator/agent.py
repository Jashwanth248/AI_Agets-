"""ADK root orchestrator.

This module is intentionally isolated from the deterministic API/tests so the
repository remains runnable without Google credentials. In a configured ADK
environment, it routes requests to specialist agents.
"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from geo_validator.agent import root_agent as geo_validator
from llm_auditor.agent import root_agent as llm_auditor

root_agent = Agent(
    name="fact_check_orchestrator",
    model="gemini-2.0-flash",
    description="Routes factual claims to specialized verification pipelines.",
    instruction=(
        "Route geographic coordinates/distance claims to geo_validator. "
        "Route general factual claims to llm_auditor. If the user is not asking "
        "for verification, answer concisely without inventing evidence."
    ),
    tools=[AgentTool(agent=geo_validator), AgentTool(agent=llm_auditor)],
)
