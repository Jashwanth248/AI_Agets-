from typing import Any, Literal
from pydantic import BaseModel, Field

class Location(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)

class ChatRequest(BaseModel):
    message: str
    location: Location | None = None
    session_id: str = "demo"

class ToolResult(BaseModel):
    tool: str
    data: Any

class ChatResponse(BaseModel):
    text: str
    intent: str
    tools: list[ToolResult] = []
    speak: bool = True
    safety_notice: str | None = None

class RouteRequest(BaseModel):
    origin: Location
    destination: Location
    travel_mode: Literal["DRIVE", "WALK", "BICYCLE"] = "DRIVE"

class RagQuery(BaseModel):
    question: str
    top_k: int = Field(default=4, ge=1, le=10)
