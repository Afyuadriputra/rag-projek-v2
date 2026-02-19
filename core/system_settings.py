from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .models import SystemSetting


DEFAULT_MAINTENANCE_MESSAGE = (
    "Kami sedang melakukan pemeliharaan terjadwal untuk meningkatkan kualitas layanan. "
    "Layanan login sementara tidak tersedia. Silakan coba kembali beberapa saat lagi."
)


@dataclass(frozen=True)
class MaintenanceState:
    enabled: bool
    message: str
    start_at: Optional[str]
    estimated_end_at: Optional[str]
    allow_staff_bypass: bool


def _iso(dt) -> Optional[str]:
    return dt.isoformat() if dt is not None else None


def get_maintenance_state() -> MaintenanceState:
    try:
        cfg = SystemSetting.objects.first()
    except Exception:
        cfg = None

    if cfg is None:
        return MaintenanceState(
            enabled=False,
            message=DEFAULT_MAINTENANCE_MESSAGE,
            start_at=None,
            estimated_end_at=None,
            allow_staff_bypass=True,
        )

    msg = cfg.get_effective_maintenance_message() or DEFAULT_MAINTENANCE_MESSAGE
    return MaintenanceState(
        enabled=bool(cfg.maintenance_enabled),
        message=msg,
        start_at=_iso(cfg.maintenance_start_at),
        estimated_end_at=_iso(cfg.maintenance_estimated_end_at),
        allow_staff_bypass=bool(cfg.allow_staff_bypass),
    )


def get_registration_enabled() -> bool:
    try:
        cfg = SystemSetting.objects.first()
    except Exception:
        cfg = None
    if cfg is None:
        return True
    return bool(cfg.registration_enabled)
