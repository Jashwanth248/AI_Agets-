from google.adk.agents import Agent, SequentialAgent
from google.adk.tools import google_search

critic = Agent(
    name="critic_agent",
    model="gemini-2.0-flash",
    instruction=(
        "Extract independently verifiable claims. Use Google Search for current or "
        "externally verifiable facts. Return claim-by-claim evidence and uncertainty."
    ),
    tools=[google_search],
    output_key="critique",
)

reviser = Agent(
    name="reviser_agent",
    model="gemini-2.0-flash",
    instruction=(
        "Using {critique}, produce a minimally corrected answer. Preserve accurate "
        "content, clearly flag uncertainty, and never fabricate citations."
    ),
)

root_agent = SequentialAgent(
    name="llm_auditor",
    description="Search-grounded critique and correction pipeline.",
    sub_agents=[critic, reviser],
)
