# backend/app/services/lead_service.py
from sqlalchemy.orm import Session
from ..models import Lead
from ..utils.id_generator import generate_lead_id

def create_or_update_lead(db: Session, lead_data: dict) -> Lead:
    """
    Check for duplicate by customer_name + mobile.
    Update if exists, create if new.
    """
    existing = db.query(Lead).filter(
        Lead.customer_name == lead_data['customer_name'],
        Lead.mobile == lead_data['mobile']
    ).first()
    
    if existing:
        # Update existing record
        for key, value in lead_data.items():
            if key not in ['customer_name', 'mobile']:
                setattr(existing, key, value)
        existing.is_duplicate = True
        db.commit()
        db.refresh(existing)
        return existing
    
    # Create new lead
    lead_id = generate_lead_id(db, lead_data['service'], lead_data['city'])
    new_lead = Lead(
        lead_id=lead_id,
        **lead_data,
        is_duplicate=False
    )
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    return new_lead
