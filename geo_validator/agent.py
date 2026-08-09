from google.adk.agents import Agent, SequentialAgent
from google.adk.tools import google_search

from geo_toolkit import compare_claimed_distance, haversine_distance_km, validate_coordinates

researcher = Agent(
    name="geo_researcher",
    model="gemini-2.0-flash",
    instruction=(
        "Research named locations and return source-grounded coordinates and any "
        "qualitative geography facts needed to verify the user's claim."
    ),
    tools=[google_search],
    output_key="geo_research",
)

calculator = Agent(
    name="geo_calculator",
    model="gemini-2.0-flash",
    instruction=(
        "Use {geo_research}. Validate coordinates and compute numeric geographic "
        "claims with deterministic tools. Do not estimate distances mentally."
    ),
    tools=[validate_coordinates, haversine_distance_km, compare_claimed_distance],
)

root_agent = SequentialAgent(
    name="geo_validator",
    description="Search-grounded geographic research plus deterministic calculation.",
    sub_agents=[researcher, calculator],
)
