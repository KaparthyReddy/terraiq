# TerraIQ — AI-Powered Soil Intelligence Platform

> Real-time soil health monitoring combining IoT sensors, Sentinel-2 satellite
> NDVI fusion, and a custom transformer model for microbiome prediction and
> precision farming recommendations.

## Architecture

```
IoT Sensors → Kafka → FastAPI backend → PostgreSQL
                  ↘                  ↘
                Redis cache      Recommendation engine
                                      ↓
                              SoilTransformer (PyTorch)
                                      ↓
                              React dashboard
```

## Stack

| Layer | Technology |
|---|---|
| API | FastAPI + asyncpg + SQLAlchemy 2.0 |
| ML | PyTorch transformer (custom NIR spectral encoder) |
| Streaming | Kafka + Redis Streams |
| Frontend | React 18 + Redux Toolkit + Recharts + Leaflet |
| Infra | AWS EKS + RDS + ElastiCache via Terraform |
| CI/CD | GitHub Actions → GHCR → kubectl rollout |

## Quick start

```bash
# 1. Clone
git clone https://github.com/YOUR_ORG/terraiq.git && cd terraiq

# 2. Copy env
cp .env.example .env

# 3. Start all services
docker compose up --build

# 4. Run migrations
docker compose exec backend alembic upgrade head

# 5. Open
#   API docs  → http://localhost:8000/docs
#   Dashboard → http://localhost:5173
```

## ML training

```bash
cd backend
pip install -r ml/requirements.txt

python -m ml.model.train \
  --data /path/to/soil_spectral.parquet \
  --output ml/model/weights/soil_transformer.pt \
  --epochs 50 \
  --batch-size 64
```

## Running tests

```bash
cd backend
pytest tests/ -v --cov=app
```

## Deployment

```bash
# Provision infra (first time)
cd infra/terraform
terraform init
terraform apply

# Deploy app (handled by CI on push to main)
git push origin main
```

## Sensor payload format

```json
{
  "field_id": "uuid",
  "sensor_id": "SNS-001",
  "ph": 6.2,
  "moisture_pct": 38.5,
  "temperature_c": 22.1,
  "nitrogen_ppm": 85,
  "phosphorus_ppm": 32,
  "potassium_ppm": 210,
  "organic_matter_pct": 3.4,
  "electrical_conductivity": 0.42,
  "spectral_signature": "0.12,0.18,0.22,..."
}
```

## License

MIT
