# Project-11
# CloudOps Sentinel

CloudOps Sentinel is a Python DevOps project that demonstrates how to build, test, containerize, and deploy a cloud-ready service.

The app exposes a small FastAPI API for cloud operations dashboards:

- `GET /health` for load balancer and Kubernetes probes
- `GET /ready` for dependency readiness checks
- `GET /metrics` for Prometheus scraping
- `GET /resources` for normalized cloud resource status
- `POST /incidents` for creating lightweight incident records

## Project Structure

```text
CloudOps Sentinel/
  app/                  FastAPI application code
  tests/                Pytest test suite
  k8s/                  Kubernetes manifests
  terraform/aws/        AWS ECS + ECR infrastructure scaffold
  .github/workflows/    CI/CD pipeline
  Dockerfile            Production container image
  docker-compose.yml    Local container run
```

## Run Locally

Install Python 3.12, then:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

## Test

```bash
pytest
```

## Run With Docker

```bash
docker build -t cloudops-sentinel:local .
docker run --rm -p 8000:8000 cloudops-sentinel:local
```

Or:

```bash
docker compose up --build
```

## Kubernetes

Update the image in `k8s/deployment.yaml`, then:

```bash
kubectl apply -f k8s/
kubectl get pods -l app=cloudops-sentinel
```

## AWS Terraform Scaffold

The Terraform files create an ECR repository and an ECS Fargate service skeleton. Configure AWS credentials first, then:

```bash
cd terraform/aws
terraform init
terraform plan
```

## CI/CD

The GitHub Actions workflow:

1. Installs dependencies
2. Runs linting and tests
3. Builds the Docker image
4. Pushes to AWS ECR on `main` when AWS secrets are configured

Required GitHub secrets for deployment:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `AWS_ACCOUNT_ID`

