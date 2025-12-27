from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum

# ==================== AUTH SCHEMAS ====================
class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# ==================== LEAD SCHEMAS ====================
class LeadCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    mobile: str = Field(..., pattern=r'^\+?[0-9]{10,15}$')
    city: str = Field(..., min_length=2, max_length=50)
    service_type: str = Field(..., min_length=2, max_length=50)
    budget_range: Optional[str] = None
    notes: Optional[str] = None

class LeadResponse(BaseModel):
    id: int
    system_lead_id: str
    full_name: str
    mobile: str
    city: str
    service_type: str
    budget_range: Optional[str]
    notes: Optional[str]
    is_duplicate: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# ==================== VENDOR SCHEMAS ====================
class VendorCreate(BaseModel):
    company_name: str = Field(..., min_length=2, max_length=100)
    owner_name: str = Field(..., min_length=2, max_length=100)
    mobile: str = Field(..., pattern=r'^\+?[0-9]{10,15}$')
    email: EmailStr
    city: str = Field(..., min_length=2, max_length=50)
    service_type: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=6)

class VendorResponse(BaseModel):
    id: int
    vendor_id: str
    company_name: str
    owner_name: str
    mobile: str
    email: str
    city: str
    service_type: str
    status: str
    credits: int
    total_leads_received: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# ==================== PAYMENT SCHEMAS ====================
class PaymentCreate(BaseModel):
    credits: int = Field(..., gt=0, description="Number of credits to purchase")

class PaymentResponse(BaseModel):
    payment_id: str
    amount: float
    credits_purchased: int
    payment_link: str
    status: str
    
    class Config:
        from_attributes = True

# ==================== LEAD ASSIGNMENT SCHEMAS ====================
class VendorLeadResponse(BaseModel):
    vendor_lead_id: str
    vendor_lead_number: int
    customer_name: str
    mobile: str
    city: str
    service_type: str
    budget_range: Optional[str]
    notes: Optional[str]
    assigned_at: datetime
    
    class Config:
        from_attributes = True
