from datetime import datetime, timezone


def utc_now() -> datetime:
    """Get current UTC time without timezone info (for SQLite compatibility)"""
    return datetime.now(timezone.utc).replace(tzinfo=None)
