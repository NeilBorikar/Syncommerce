from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.api.dependencies import get_current_user
from app.core.database import mongo
from app.repositories.query_repository import QueryRepository
from app.models.query_model import PatientQuery
from app.schemas.query_schema import QueryCreate, QueryAnswer, QueryForward, QueryResponse

router = APIRouter()

def get_query_repo():
    return QueryRepository(mongo.db)

@router.post("/", response_model=QueryResponse)
def create_query(
    data: QueryCreate,
    current_user: dict = Depends(get_current_user),
    query_repo: QueryRepository = Depends(get_query_repo)
):
    if current_user.get("role") != "patient":
        raise HTTPException(status_code=403, detail="Only patients can submit queries")
        
    query = PatientQuery(
        business_id=current_user.get("business_id"),
        patient_id=current_user["_id"],
        question_text=data.question_text
    )
    
    q_id = query_repo.create(query.__dict__)
    return query_repo.get_by_id(q_id)

@router.get("/", response_model=List[QueryResponse])
def get_queries(
    current_user: dict = Depends(get_current_user),
    query_repo: QueryRepository = Depends(get_query_repo)
):
    role = current_user.get("role")
    
    if role == "patient":
        return query_repo.get_by_patient(current_user["_id"])
        
    # Clinic staff
    queries = query_repo.get_by_business(current_user.get("business_id"))
    
    if role == "doctor":
        # Doctors only see forwarded queries
        return [q for q in queries if q.get("forwarded_to") == current_user["_id"] or q.get("answered_by") == current_user["_id"]]
        
    return queries

@router.put("/{query_id}/answer", response_model=QueryResponse)
def answer_query(
    query_id: str,
    data: QueryAnswer,
    current_user: dict = Depends(get_current_user),
    query_repo: QueryRepository = Depends(get_query_repo)
):
    role = current_user.get("role")
    if role not in ["nurse", "receptionist", "doctor", "owner"]:
        raise HTTPException(status_code=403, detail="Not authorized to answer queries")
        
    query = query_repo.get_by_id(query_id)
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
        
    if role == "doctor" and query.get("forwarded_to") != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Doctor can only answer forwarded queries")
        
    query_repo.update(query_id, {
        "status": "answered",
        "answer_text": data.answer_text,
        "answered_by": current_user["_id"]
    })
    
    return query_repo.get_by_id(query_id)

@router.put("/{query_id}/forward", response_model=QueryResponse)
def forward_query(
    query_id: str,
    data: QueryForward,
    current_user: dict = Depends(get_current_user),
    query_repo: QueryRepository = Depends(get_query_repo)
):
    role = current_user.get("role")
    if role not in ["nurse", "receptionist", "owner"]:
        raise HTTPException(status_code=403, detail="Only nurse or receptionist can forward queries")
        
    query = query_repo.get_by_id(query_id)
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
        
    query_repo.update(query_id, {
        "status": "forwarded",
        "forwarded_to": data.forwarded_to
    })
    
    return query_repo.get_by_id(query_id)
