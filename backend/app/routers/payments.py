# backend/app/routers/payments.py
from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
import razorpay
import hmac
import hashlib
from ..database import get_db
from ..config import settings
from ..models import Payment, Vendor
from ..services.payment_service import generate_invoice

router = APIRouter()
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@router.post("/webhook/razorpay")
async def razorpay_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle Razorpay payment webhook"""
    body = await request.body()
    signature = request.headers.get("X-Razorpay-Signature")
    
    # Verify signature
    expected_signature = hmac.new(
        settings.RAZORPAY_WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    
    if signature != expected_signature:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    data = await request.json()
    
    if data['event'] == 'payment.captured':
        payment_id = data['payload']['payment']['entity']['id']
        amount = data['payload']['payment']['entity']['amount'] / 100  # Razorpay sends in paise
        
        # Find payment record
        payment = db.query(Payment).filter(
            Payment.gateway_payment_id == payment_id
        ).first()
        
        if payment:
            payment.status = "completed"
            
            # Credit vendor
            vendor = db.query(Vendor).filter(Vendor.id == payment.vendor_id).first()
            vendor.credits += payment.credits_purchased
            vendor.is_active = True  # Re-activate vendor
            
            # Generate invoice
            invoice_url = generate_invoice(payment, vendor)
            payment.invoice_url = invoice_url
            
            db.commit()
    
    return {"status": "ok"}
