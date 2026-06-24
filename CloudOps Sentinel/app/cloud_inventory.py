from app.models import CloudResource, ResourceState


def list_resources() -> list[CloudResource]:
    return [
        CloudResource(
            id="ecs-api-001",
            name="sentinel-api",
            type="ecs-service",
            region="us-east-1",
            state=ResourceState.healthy,
            cost_per_hour_usd=0.048,
        ),
        CloudResource(
            id="rds-main-001",
            name="sentinel-postgres",
            type="rds-instance",
            region="us-east-1",
            state=ResourceState.degraded,
            cost_per_hour_usd=0.115,
        ),
        CloudResource(
            id="s3-logs-001",
            name="sentinel-access-logs",
            type="s3-bucket",
            region="us-east-1",
            state=ResourceState.healthy,
            cost_per_hour_usd=0.006,
        ),
    ]


def readiness_report() -> dict[str, str]:
    resources = list_resources()
    degraded = [resource for resource in resources if resource.state != ResourceState.healthy]
    if degraded:
        return {"status": "degraded", "details": f"{len(degraded)} resource(s) need attention"}
    return {"status": "ready", "details": "all resources healthy"}

