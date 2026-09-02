from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Lock
from uuid import uuid4


def _now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class AnalyticsEvent:
    event_id: str
    tenant_id: str
    engine: str
    event_type: str
    created_at: datetime = field(default_factory=_now)


_analytics_lock = Lock()
_analytics_by_tenant_engine: dict[str, dict[str, list[AnalyticsEvent]]] = {}


def record_event(tenant_id: str, engine: str, event_type: str) -> dict:
    with _analytics_lock:
        tenant_map = _analytics_by_tenant_engine.setdefault(tenant_id, {})
        events = tenant_map.setdefault(engine, [])
        event = AnalyticsEvent(
            event_id=str(uuid4()),
            tenant_id=tenant_id,
            engine=engine,
            event_type=event_type,
        )
        events.append(event)
        return {
            "event_id": event.event_id,
            "tenant_id": event.tenant_id,
            "engine": event.engine,
            "event_type": event.event_type,
            "created_at": event.created_at,
        }


def get_engine_events(tenant_id: str, engine: str) -> list[dict]:
    with _analytics_lock:
        tenant_map = _analytics_by_tenant_engine.get(tenant_id, {})
        return [
            {
                "event_id": event.event_id,
                "tenant_id": event.tenant_id,
                "engine": event.engine,
                "event_type": event.event_type,
                "created_at": event.created_at,
            }
            for event in tenant_map.get(engine, [])
        ]


def get_tenant_analytics_snapshot(tenant_id: str) -> dict:
    with _analytics_lock:
        tenant_map = _analytics_by_tenant_engine.get(tenant_id, {})
        return {
            "tenant_id": tenant_id,
            "engines": {
                engine: {
                    "event_count": len(events),
                    "last_event_at": events[-1].created_at if events else None,
                }
                for engine, events in tenant_map.items()
            },
        }
