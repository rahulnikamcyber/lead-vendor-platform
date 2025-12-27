from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base

class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    REFUNDED = "refunded"

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(String, unique=True, index=True, nullable=False)
    
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    
    amount = Column(Float, nullable=False)
    currency = Column(String, default="INR")
    credits_purchased = Column(Integer, nullable=False)
    
    # Razorpay fields
    razorpay_order_id = Column(String, nullable=True)
    razorpay_payment_id = Column(String, nullable=True)
    razorpay_signature = Column(String, nullable=True)
    
    payment_link = Column(String, nullable=True)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    
    invoice_number = Column(String, nullable=True)
    invoice_path = Column(String, nullable=True)
    
    metadata = Column(Text, nullable=True)  # JSON string for additional data
    
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    vendor = relationship("Vendor", back_populates="payments")
