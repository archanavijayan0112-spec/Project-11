from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field


class ResourceState(str, Enum):
    healthy = "healthy"
    degraded = "degraded"
    critical = "critical"


class CloudResource(BaseModel):
    id: str
    name: str
    type: str
    region: str
    state: ResourceState
    cost_per_hour_usd: float = Field(ge=0)


class IncidentCreate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    severity: str = Field(pattern="^(low|medium|high|critical)$")
    resource_id: str


class Incident(BaseModel):
    id: str
    title: str
    severity: str
    resource_id: str
    created_at: datetime


def utc_now() -> datetime:
    return datetime.now(timezone.utc)

