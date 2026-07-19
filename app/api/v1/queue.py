from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import datetime, timezone
from app.api.dependencies import get_current_user
from app.core.database import mongo
from app.repositories.queue_repository import QueueRepository
from app.repositories.appointment_repository import AppointmentRepository
from app.models.queue_model import Queue
from app.models.appointment_model import Appointment
from app.schemas.queue_schema import QueueResponse
from app.schemas.appointment_schema import AppointmentCreate, AppointmentResponse

router = APIRouter()

def get_queue_repo():
    return QueueRepository(mongo.db)

def get_appointment_repo():
    return AppointmentRepository(mongo.db)

@router.post("/book", response_model=AppointmentResponse)
def book_appointment(
    data: AppointmentCreate,
    current_user: dict = Depends(get_current_user),
    queue_repo: QueueRepository = Depends(get_queue_repo),
    appointment_repo: AppointmentRepository = Depends(get_appointment_repo)
):
    if current_user.get("role") != "patient":
        raise HTTPException(status_code=403, detail="Only patients can book appointments")
        
    business_id = current_user.get("business_id")
    if not business_id:
        raise HTTPException(status_code=400, detail="Patient is not associated with a clinic")
        
    date_today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    # Check if already booked today
    existing = appointment_repo.get_patient_appointment(current_user["_id"], date_today)
    if existing:
        return existing
        
    # Get all appointments for today to assign next token
    appointments_today = appointment_repo.get_by_business_and_date(business_id, date_today)
    next_token = len(appointments_today) + 1
    
    # Ensure queue exists for today
    queue = queue_repo.get_by_business_and_date(business_id, date_today)
    if not queue:
        new_queue = Queue(business_id=business_id, date=date_today)
        queue_repo.create(new_queue.__dict__)
        
    appointment = Appointment(
        business_id=business_id,
        patient_id=current_user["_id"],
        token_number=next_token,
        slot_time=data.slot_time
    )
    
    app_id = appointment_repo.create(appointment.__dict__)
    return appointment_repo.get_by_id(app_id)

@router.get("/status", response_model=dict)
def get_queue_status(
    current_user: dict = Depends(get_current_user),
    queue_repo: QueueRepository = Depends(get_queue_repo),
    appointment_repo: AppointmentRepository = Depends(get_appointment_repo)
):
    business_id = current_user.get("business_id")
    date_today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    queue = queue_repo.get_by_business_and_date(business_id, date_today)
    current_token = queue["current_token"] if queue else 0
    avg_wait = queue["avg_wait_minutes"] if queue else 15
    
    response = {
        "current_token": current_token,
        "your_token": None,
        "estimated_wait_minutes": 0
    }
    
    if current_user.get("role") == "patient":
        appointment = appointment_repo.get_patient_appointment(current_user["_id"], date_today)
        if appointment:
            token = appointment["token_number"]
            response["your_token"] = token
            if token > current_token:
                response["estimated_wait_minutes"] = (token - current_token) * avg_wait
                
    return response

@router.post("/next", response_model=QueueResponse)
def advance_queue(
    current_user: dict = Depends(get_current_user),
    queue_repo: QueueRepository = Depends(get_queue_repo)
):
    if current_user.get("role") not in ["doctor", "nurse", "receptionist", "owner"]:
        raise HTTPException(status_code=403, detail="Not authorized to advance queue")
        
    business_id = current_user.get("business_id")
    date_today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    queue = queue_repo.get_by_business_and_date(business_id, date_today)
    if not queue:
        new_queue = Queue(business_id=business_id, date=date_today)
        q_id = queue_repo.create(new_queue.__dict__)
        queue = queue_repo.get_by_id(q_id)
        
    new_token = queue["current_token"] + 1
    queue_repo.update(queue["id"], {"current_token": new_token})
    
    return queue_repo.get_by_id(queue["id"])
