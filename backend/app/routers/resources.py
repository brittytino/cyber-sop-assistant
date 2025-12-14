"""
Resources Router - Handles cybercrime resources and reporting links
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

from ..dependencies import get_db
from ..schemas import ResourceOut, ResourceCreate
from ..models import Resource

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", response_model=List[ResourceOut])
async def get_resources(db: Session = Depends(get_db)):
    """
    Get all cybercrime resources
    """
    resources = db.query(Resource).order_by(Resource.order, Resource.category).all()
    return resources

@router.post("/", response_model=ResourceOut)
async def create_resource(resource: ResourceCreate, db: Session = Depends(get_db)):
    """
    Create a new resource (admin only)
    """
    db_resource = Resource(**resource.dict())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

@router.delete("/{resource_id}")
async def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    """
    Delete a resource (admin only)
    """
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    db.delete(resource)
    db.commit()
    return {"message": "Resource deleted successfully"}

@router.post("/initialize")
async def initialize_resources(db: Session = Depends(get_db)):
    """
    Initialize default resources in database
    """
    # Check if resources already exist
    count = db.query(Resource).count()
    if count > 0:
        return {"message": f"Resources already exist ({count} resources)", "initialized": False}
    
    # Add default resources
    from ..seed_data import RESOURCES
    for res_data in RESOURCES:
        resource = Resource(**res_data)
        db.add(resource)
    
    db.commit()
    return {"message": f"Initialized {len(RESOURCES)} resources", "initialized": True}
