# backend/app/services/routing_engine.py
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..models import Vendor, VendorLeadMap, Lead, LeadRoutingLog
from .notification_service import send_lead_notification

def route_lead_to_vendors(db: Session, lead: Lead):
    """
    Route lead to active vendors with credits > 0
    matching service and city.
    """
    vendors = db.query(Vendor).filter(
        and_(
            Vendor.service == lead.service,
            Vendor.city == lead.city,
            Vendor.is_active == True,
            Vendor.credits > 0
        )
    ).all()
    
    for vendor in vendors:
        # Get next vendor lead number
        max_number = db.query(VendorLeadMap).filter(
            VendorLeadMap.vendor_id == vendor.id
        ).count()
        
        vendor_lead_number = max_number + 1
        
        # Create mapping
        mapping = VendorLeadMap(
            vendor_id=vendor.id,
            lead_id=lead.id,
            vendor_lead_number=vendor_lead_number
        )
        db.add(mapping)
        
        # Deduct credit
        vendor.credits -= 1
        
        # Auto-disable if credits exhausted
        if vendor.credits == 0:
            vendor.is_active = False
        
        # Send notification
        status = send_lead_notification(vendor, lead, vendor_lead_number)
        
        # Log routing
        log = LeadRoutingLog(
            lead_id=lead.id,
            vendor_id=vendor.id,
            status=status,
            delivery_method="whatsapp,email",
            credits_deducted=1
        )
        db.add(log)
    
    db.commit()
