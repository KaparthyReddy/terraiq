import asyncio
import json

from aiokafka import AIOKafkaConsumer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logging import setup_logging
from app.db.session import AsyncSessionLocal
from app.models.sensor_reading import SensorReading
from app.services.recommendation_engine import maybe_trigger_recommendation
from app.services.sensor_ingest import cache_latest_reading

import structlog

log = structlog.get_logger()


async def consume():
    setup_logging()
    consumer = AIOKafkaConsumer(
        settings.KAFKA_SENSOR_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id="terraiq-sensor-group",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
    )

    await consumer.start()
    log.info("kafka_consumer.started", topic=settings.KAFKA_SENSOR_TOPIC)

    try:
        async for msg in consumer:
            payload = msg.value
            log.info("kafka_consumer.message", field_id=payload.get("field_id"))

            async with AsyncSessionLocal() as db:
                reading = SensorReading(**payload)
                db.add(reading)
                await db.commit()
                await db.refresh(reading)
                await cache_latest_reading(reading)
                await maybe_trigger_recommendation(reading, db)

    except asyncio.CancelledError:
        log.info("kafka_consumer.stopping")
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume())
