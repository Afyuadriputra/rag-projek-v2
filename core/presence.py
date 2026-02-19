from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
import random

from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.utils import timezone

from .models import UserLoginPresence

ONLINE_WINDOW_MINUTES = 15
PRESENCE_TOUCH_THROTTLE_SECONDS = 60


@dataclass(frozen=True)
class PresenceSummary:
    active_online_non_staff_count: int
    online_users: list[dict]
    recent_registered_users: list[dict]


def get_online_threshold(now=None):
    now = now or timezone.now()
    return now - timedelta(minutes=ONLINE_WINDOW_MINUTES)


def cleanup_stale_presence(now=None) -> int:
    now = now or timezone.now()
    threshold = get_online_threshold(now=now)
    return UserLoginPresence.objects.filter(
        is_active=True,
        last_seen_at__lt=threshold,
    ).update(
        is_active=False,
        logged_out_at=now,
    )


def maybe_cleanup_stale_presence(chance: float = 0.01) -> int:
    if random.random() > chance:
        return 0
    return cleanup_stale_presence()


def mark_presence_login(
    *,
    user: User,
    session_key: str,
    ip_address: str = "",
    user_agent: str = "",
    now=None,
) -> UserLoginPresence | None:
    if not session_key:
        return None
    now = now or timezone.now()
    obj, _ = UserLoginPresence.objects.update_or_create(
        session_key=session_key,
        defaults={
            "user": user,
            "ip_address": (ip_address or "")[:64],
            "user_agent": (user_agent or "")[:512],
            "is_active": True,
            "logged_out_at": None,
            "last_seen_at": now,
        },
    )
    return obj


def mark_presence_inactive(*, session_key: str, now=None) -> int:
    if not session_key:
        return 0
    now = now or timezone.now()
    return UserLoginPresence.objects.filter(session_key=session_key, is_active=True).update(
        is_active=False,
        logged_out_at=now,
    )


def touch_presence(
    *,
    session_key: str,
    now=None,
    throttle_seconds: int = PRESENCE_TOUCH_THROTTLE_SECONDS,
) -> bool:
    if not session_key:
        return False
    now = now or timezone.now()
    threshold = now - timedelta(seconds=throttle_seconds)
    updated = UserLoginPresence.objects.filter(
        session_key=session_key,
        is_active=True,
        last_seen_at__lt=threshold,
    ).update(last_seen_at=now)
    return bool(updated)


def active_presence_qs(now=None) -> QuerySet[UserLoginPresence]:
    threshold = get_online_threshold(now=now)
    return UserLoginPresence.objects.filter(
        is_active=True,
        last_seen_at__gte=threshold,
    )


def count_active_online_non_staff_users(now=None) -> int:
    return (
        active_presence_qs(now=now)
        .filter(user__is_staff=False, user__is_superuser=False)
        .values("user_id")
        .distinct()
        .count()
    )


def is_user_online_non_staff(user: User, now=None) -> bool:
    if not user or user.is_staff or user.is_superuser:
        return False
    return (
        active_presence_qs(now=now)
        .filter(user_id=user.id, user__is_staff=False, user__is_superuser=False)
        .exists()
    )


def build_presence_summary(limit: int = 100, now=None) -> PresenceSummary:
    now = now or timezone.now()

    online_rows = (
        active_presence_qs(now=now)
        .select_related("user")
        .filter(user__is_staff=False, user__is_superuser=False)
        .order_by("-last_seen_at")[:1000]
    )

    seen_user_ids = set()
    online_users: list[dict] = []
    for row in online_rows:
        if row.user_id in seen_user_ids:
            continue
        seen_user_ids.add(row.user_id)
        online_users.append(
            {
                "user_id": row.user_id,
                "username": row.user.username,
                "is_staff": bool(row.user.is_staff or row.user.is_superuser),
                "ip_address": row.ip_address,
                "logged_in_at": row.logged_in_at.isoformat() if row.logged_in_at else None,
                "last_seen_at": row.last_seen_at.isoformat() if row.last_seen_at else None,
            }
        )
        if len(online_users) >= limit:
            break

    recent_users = (
        User.objects.order_by("-date_joined")
        .only("id", "username", "is_staff", "is_superuser", "date_joined")[:limit]
    )
    recent_registered_users = [
        {
            "user_id": u.id,
            "username": u.username,
            "is_staff": bool(u.is_staff or u.is_superuser),
            "date_joined": u.date_joined.isoformat() if u.date_joined else None,
        }
        for u in recent_users
    ]

    return PresenceSummary(
        active_online_non_staff_count=count_active_online_non_staff_users(now=now),
        online_users=online_users,
        recent_registered_users=recent_registered_users,
    )
