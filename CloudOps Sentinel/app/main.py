from uuid import uuid4
from fastapi import FastAPI, Response, status

from app.cloud_inventory import list_resources, readiness_report
from app.config import get_settings
from app.models import Incident, IncidentCreate, utc_now

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="A cloud-ready Python DevOps sample service.",
)

incidents: list[Incident] = []


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": settings.app_name,
        "environment": settings.environment,
        "cloud_provider": settings.cloud_provider,
        "version": settings.version,
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
def ready(response: Response) -> dict[str, str]:
    report = readiness_report()
    if report["status"] != "ready":
        response.status_code = status.HTTP_200_OK
    return report


@app.get("/resources")
def resources():
    return {"items": list_resources()}


@app.post("/incidents", status_code=status.HTTP_201_CREATED)
def create_incident(payload: IncidentCreate) -> Incident:
    incident = Incident(
        id=str(uuid4()),
        title=payload.title,
        severity=payload.severity,
        resource_id=payload.resource_id,
        created_at=utc_now(),
    )
    incidents.append(incident)
    return incident


@app.get("/incidents")
def list_incidents() -> dict[str, list[Incident]]:
    return {"items": incidents}


@app.get("/metrics")
def metrics() -> Response:
    resources_snapshot = list_resources()
    total_hourly_cost = sum(resource.cost_per_hour_usd for resource in resources_snapshot)
    degraded_count = sum(resource.state != "healthy" for resource in resources_snapshot)
    body = "\n".join(
        [
            "# HELP cloudops_resources_total Total tracked cloud resources.",
            "# TYPE cloudops_resources_total gauge",
            f"cloudops_resources_total {len(resources_snapshot)}",
            "# HELP cloudops_degraded_resources_total Total degraded or critical resources.",
            "# TYPE cloudops_degraded_resources_total gauge",
            f"cloudops_degraded_resources_total {degraded_count}",
            "# HELP cloudops_hourly_cost_usd Estimated hourly cloud cost.",
            "# TYPE cloudops_hourly_cost_usd gauge",
            f"cloudops_hourly_cost_usd {total_hourly_cost:.3f}",
        ]
    )
    return Response(content=f"{body}\n", media_type="text/plain")

