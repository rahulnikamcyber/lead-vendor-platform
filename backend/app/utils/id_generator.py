from datetime import datetime
from sqlalchemy.orm import Session
from ..models import LeadSequence, VendorSequence

def generate_lead_id(db: Session, service: str, city: str) -> str:
    """
    Generate auto Lead ID: LD-<SERVICE>-<CITY>-<DDYYYYMM>-<SEQ>
    Example: LD-SOLAR-SURAT-27202512-004
    """
    now = datetime.now()
    date_key = now.strftime("%d%Y%m")  # DDYYYYMM
    
    # Get or create sequence
    seq = db.query(LeadSequence).filter(
        LeadSequence.service == service.upper(),
        LeadSequence.city == city.upper(),
        LeadSequence.date_key == date_key
    ).first()
    
    if not seq:
        seq = LeadSequence(
            service=service.upper(),
            city=city.upper(),
            date_key=date_key,
            sequence=1
        )
        db.add(seq)
    else:
        seq.sequence += 1
    
    db.commit()
    
    lead_id = f"LD-{service.upper()}-{city.upper()}-{date_key}-{seq.sequence:03d}"
    return lead_id

def generate_vendor_id(db: Session, service: str, city: str) -> str:
    """
    Generate vendor ID: VD-<SERVICE>-<CITY>-<NUMBER>
    Example: VD-SOLAR-SURAT-001
    """
    seq = db.query(VendorSequence).filter(
        VendorSequence.service == service.upper(),
        VendorSequence.city == city.upper()
    ).first()
    
    if not seq:
        seq = VendorSequence(
            service=service.upper(),
            city=city.upper(),
            sequence=1
        )
        db.add(seq)
    else:
        seq.sequence += 1
    
    db.commit()
    
    vendor_id = f"VD-{service.upper()}-{city.upper()}-{seq.sequence:03d}"
    return vendor_id
