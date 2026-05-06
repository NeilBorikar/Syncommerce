from enum import Enum
from typing import Dict, Any


class EventType(str, Enum):
    # Billing
    BILL_CREATED = "BILL_CREATED"
    BILL_UPDATED = "BILL_UPDATED"

    # Drafts
    DRAFT_CREATED = "DRAFT_CREATED"
    DRAFT_UPDATED = "DRAFT_UPDATED"

    # Inventory
    INVENTORY_UPDATED = "INVENTORY_UPDATED"

    # System
    USER_JOINED = "USER_JOINED"
    USER_LEFT = "USER_LEFT"


def build_event(event_type: EventType, payload: Dict[str, Any]):
    """
    Standard event structure
    """
    return {
        "type": event_type,
        "payload": payload
    }