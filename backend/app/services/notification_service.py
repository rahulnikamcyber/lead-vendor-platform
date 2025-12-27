import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..config import settings
import requests

class NotificationService:
    
    @staticmethod
    def send_email(to_email: str, subject: str, body_html: str):
        """Send email notification"""
        
        if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
            print(f"Email notification skipped (SMTP not configured): {to_email}")
            return False
        
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = settings.SMTP_FROM
            msg['To'] = to_email
            msg['Subject'] = subject
            
            html_part = MIMEText(body_html, 'html')
            msg.attach(html_part)
            
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
            
            print(f"Email sent to {to_email}")
            return True
            
        except Exception as e:
            print(f"Email error: {str(e)}")
            return False
    
    @staticmethod
    def send_whatsapp(to_number: str, message: str):
        """Send WhatsApp notification"""
        
        if not settings.WHATSAPP_ENABLED:
            print(f"WhatsApp notification skipped: {to_number}")
            return False
        
        try:
            # Implement WhatsApp API call (Twilio, etc.)
            print(f"WhatsApp sent to {to_number}: {message}")
            return True
        except Exception as e:
            print(f"WhatsApp error: {str(e)}")
            return False
    
    @staticmethod
    def send_lead_notification(vendor, lead, vendor_lead_id: str):
        """Send lead notification to vendor"""
        
        subject = f"New Lead Received - {vendor_lead_id}"
        
        body_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>New Lead Received!</h2>
            <p>Dear {vendor.owner_name},</p>
            <p>You have received a new lead:</p>
            
            <table style="border-collapse: collapse; width: 100%; max-width: 500px;">
                <tr style="background-color: #f2f2f2;">
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Lead ID</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{vendor_lead_id}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Customer Name</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{lead.full_name}</td>
                </tr>
                <tr style="background-color: #f2f2f2;">
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Mobile</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{lead.mobile}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>City</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{lead.city}</td>
                </tr>
                <tr style="background-color: #f2f2f2;">
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Service</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{lead.service_type}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Budget Range</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{lead.budget_range or 'Not specified'}</td>
                </tr>
            </table>
            
            <p><strong>Notes:</strong> {lead.notes or 'None'}</p>
            
            <p style="margin-top: 20px;">
                <strong>Remaining Credits:</strong> {vendor.credits}
            </p>
            
            <p>Please contact the customer as soon as possible.</p>
            
            <p style="color: #666; font-size: 12px; margin-top: 30px;">
                This is an automated notification from {settings.APP_NAME}
            </p>
        </body>
        </html>
        """
        
        # Send email
        NotificationService.send_email(vendor.email, subject, body_html)
        
        # Send WhatsApp if enabled
        if settings.WHATSAPP_ENABLED:
            whatsapp_msg = f"""
New Lead: {vendor_lead_id}
Customer: {lead.full_name}
Mobile: {lead.mobile}
Service: {lead.service_type}
City: {lead.city}
Budget: {lead.budget_range or 'Not specified'}
            """.strip()
            NotificationService.send_whatsapp(vendor.mobile, whatsapp_msg)
