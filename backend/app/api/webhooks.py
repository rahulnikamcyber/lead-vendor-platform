from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.payment_service import PaymentService
import hmac
import hashlib

router = APIRouter(prefix="/api/webhooks", tags=["Webhooks"])

@router.post("/razorpay")
async def razorpay_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """Handle Razorpay webhook for payment verification"""
    
    try:
        # Get webhook payload
        payload = await request.body()
        signature = request.headers.get("X-Razorpay-Signature")
        
        # Verify signature (in production)
        # webhook_secret = settings.RAZORPAY_WEBHOOK_SECRET
        # expected_signature = hmac.new(
        #     webhook_secret.encode(),
        #     payload,
        #     hashlib.sha256
        # ).hexdigest()
        # 
        # if signature != expected_signature:
        #     raise HTTPException(status_code=400, detail="Invalid signature")
        
        # Parse webhook data
        data = await request.json()
        event = data.get("event")
        
        if event == "payment.captured":
            payment_entity = data.get("payload", {}).get("payment", {}).get("entity", {})
            
            # Extract payment details
            razorpay_payment_id = payment_entity.get("id")
            razorpay_order_id = payment_entity.get("order_id")
            
            # Find payment by order ID
            from ..models.payment import Payment
            payment = db.query(Payment).filter(
                Payment.razorpay_order_id == razorpay_order_id
            ).first()
            
            if payment:
                payment_service = PaymentService()
                payment_service.verify_payment(
                    db,
                    payment.payment_id,
                    razorpay_payment_id,
                    signature or ""
                )
        
        return {"status": "ok"}
        
    except Exception as e:
        print(f"Webhook error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/payment")
async def payment_callback(
    payment_id: str = None,
    razorpay_payment_id: str = None,
    razorpay_order_id: str = None,
    razorpay_signature: str = None,
    db: Session = Depends(get_db)
):
    """Handle payment callback (demo mode)"""
    
    try:
        if not payment_id:
            raise HTTPException(status_code=400, detail="Payment ID required")
        
        payment_service = PaymentService()
        payment = payment_service.verify_payment(
            db,
            payment_id,
            razorpay_payment_id or "demo_payment_id",
            razorpay_signature or "demo_signature"
        )
        
        return {
            "success": True,
            "message": "Payment successful",
            "payment_id": payment.payment_id,
            "credits_added": payment.credits_purchased
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
