import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional
import asyncio


# -------------------------------
# ID GENERATION
# -------------------------------
def generate_uuid() -> str:
    """
    Generate a unique ID
    """
    return str(uuid.uuid4())


# -------------------------------
# TIME UTILITIES
# -------------------------------
def get_current_utc() -> datetime:
    """
    Get current UTC timestamp
    """
    return datetime.now(timezone.utc)


def format_datetime(dt: datetime) -> str:
    """
    Convert datetime to ISO format string
    """
    return dt.isoformat()


# -------------------------------
# RESPONSE FORMATTER
# -------------------------------
def success_response(
    data: Any = None,
    message: str = "Success",
) -> Dict[str, Any]:
    return {
        "status": "success",
        "message": message,
        "data": data,
        "timestamp": format_datetime(get_current_utc()),
    }


def error_response(
    message: str = "Something went wrong",
    error: Optional[Any] = None,
) -> Dict[str, Any]:
    return {
        "status": "error",
        "message": message,
        "error": str(error) if error else None,
        "timestamp": format_datetime(get_current_utc()),
    }


# -------------------------------
# DATA CLEANING
# -------------------------------
def remove_none_values(data: Dict) -> Dict:
    """
    Remove None values from dict
    """
    return {k: v for k, v in data.items() if v is not None}


# -------------------------------
# ASYNC HELPERS
# -------------------------------
async def run_in_background(func, *args, **kwargs):
    """
    Run blocking function in async background
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func, *args)


# -------------------------------
# PAGINATION
# -------------------------------
def paginate(page: int = 1, limit: int = 10):
    """
    Return skip and limit for DB queries
    """
    skip = (page - 1) * limit
    return skip, limit


# -------------------------------
# SAFE DICT ACCESS
# -------------------------------
def safe_get(data: Dict, key: str, default=None):
    """
    Safe dictionary access
    """
    return data.get(key, default)