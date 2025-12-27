# Lead-Vendor Automation Platform

A complete lead distribution automation system that connects customers with service vendors automatically.

## 🚀 Features

### Core Features
- ✅ **Automated Lead Routing** - Matches leads with vendors based on city and service type
- ✅ **Unique ID Generation** - System-level and vendor-specific lead IDs
- ✅ **No Manual Dates** - All dates are system-generated
- ✅ **Duplicate Detection** - Prevents duplicate leads using name + mobile
- ✅ **Credit System** - Vendors purchase credits, 1 credit = 1 lead
- ✅ **Role-Based Access** - Admin and Vendor dashboards
- ✅ **Responsive Design** - Works on mobile, tablet, and desktop
- ✅ **Payment Integration** - Razorpay with webhook verification
- ✅ **Notifications** - Email and WhatsApp delivery
- ✅ **Real-time Analytics** - Charts and statistics

### ID System
```
Lead ID Format: LD-SOLAR-SURAT-27202512-004
- LD: Lead prefix
- SOLAR: Service type
- SURAT: City
- 27202512: Date (DDYYYYMM)
- 004: Sequential number

Vendor ID Format: VD-SOLAR-SURAT-001
- VD: Vendor prefix
- SOLAR: Service type
- SURAT: City
- 001: Sequential number

Vendor Lead ID: Lead #001, Lead #002, etc.
(Vendor cannot see total platform leads)
```

## 📋 Tech Stack

**Backend:**
- Python 3.10+
- FastAPI
- SQLAlchemy
- PostgreSQL / SQLite
- JWT Authentication
- APScheduler

**Frontend:**
- HTML5
- Tailwind CSS
- Chart.js
- Vanilla JavaScript

**Integrations:**
- Razorpay (Payments)
- SMTP (Email)
- WhatsApp API (Optional)

## 🛠️ Installation

### Prerequisites
```bash
- Python 3.10 or higher
- pip
- PostgreSQL (optional, SQLite works for demo)
```

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/lead-vendor-platform.git
cd lead-vendor-platform
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

**Important Environment Variables:**
```env
DATABASE_URL=sqlite:///./lead_vendor.db
SECRET_KEY=your-very-long-secret-key-change-this
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=Admin@123

# For Razorpay (optional for demo)
RAZORPAY_KEY_ID=your_key
RAZORPAY_KEY_SECRET=your_secret

# For Email (optional for demo)
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### Step 5: Initialize Database
```bash
# Database will be created automatically on first run
python -m backend.app.main
```

### Step 6: Run Application
```bash
# Using Python
python -m uvicorn backend.app.main:app --reload --port 8000

# Or using the run script
python run.py
```

### Step 7: Access Application
```
🌐 Application: http://localhost:8000
📚 API Docs: http://localhost:8000/docs
👤 Admin Login: admin@example.com / Admin@123
```

## 📁 Project Structure

```
lead-vendor-platform/
├── backend/
│   └── app/
│       ├── main.py                 # FastAPI application
│       ├── config.py               # Configuration
│       ├── database.py             # Database setup
│       ├── models/                 # SQLAlchemy models
│       │   ├── user.py
│       │   ├── vendor.py
│       │   ├── lead.py
│       │   ├── payment.py
│       │   └── lead_assignment.py
│       ├── schemas/                # Pydantic schemas
│       ├── api/                    # API routes
│       │   ├── auth.py
│       │   ├── leads.py
│       │   ├── vendor.py
│       │   ├── admin.py
│       │   └── webhooks.py
│       └── services/               # Business logic
│           ├── auth_service.py
│           ├── lead_service.py
│           ├── vendor_service.py
│           ├── payment_service.py
│           ├── id_generator.py
│           ├── lead_router.py
│           └── notification_service.py
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── login.html
│       ├── forms/
│       │   ├── lead_form.html
│       │   └── vendor_registration.html
│       ├── admin/
│       │   └── dashboard.html
│       └── vendor/
│           └── dashboard.html
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── run.py
```

## 🔐 Default Credentials

**Admin Account:**
- Email: admin@example.com
- Password: Admin@123

*Change these in production!*

## 📊 Database Schema

### Users Table
- id, email, hashed_password, role, is_active
- Roles: admin, vendor

### Vendors Table
- vendor_id (VD-SERVICE-CITY-SEQ)
- company_name, owner_name, mobile, email
- city, service_type
- status (inactive/active/suspended)
- credits, total_leads_received

### Leads Table
- system_lead_id (LD-SERVICE-CITY-DATE-SEQ)
- full_name, mobile, city, service_type
- budget_range, notes
- is_duplicate, original_lead_id

### Lead Assignments Table
- lead_id, vendor_id
- vendor_lead_number (1, 2, 3...)
- vendor_lead_id ("Lead #001")
- credits_deducted, is_delivered

### Payments Table
- payment_id, vendor_id
- amount, credits_purchased
- razorpay_order_id, razorpay_payment_id
- status, invoice_number

## 🎯 Usage Guide

### For Customers

1. **Submit a Lead**
   - Go to `/lead-form`
   - Fill in requirements
   - No need to enter date or ID
   - System automatically routes to vendors

### For Vendors

1. **Register**
   - Go to `/vendor-registration`
   - Fill company details
   - Account created as INACTIVE with 0 credits

2. **Purchase Credits**
   - Login to dashboard
   - Click "Buy Credits"
   - Complete payment via Razorpay
   - Credits added automatically
   - Account activated

3. **Receive Leads**
   - Leads automatically sent to email/WhatsApp
   - View in dashboard
   - Each lead shows as "Lead #001", "Lead #002"
   - 1 credit deducted per lead

### For Admins

1. **Dashboard**
   - View total leads, vendors, revenue
   - Charts for leads by city/service
   - Duplicate lead detection

2. **Manage Vendors**
   - View all vendors
   - Manually add/remove credits
   - Activate/deactivate vendors

3. **Lead Routing Logs**
   - Track which leads went to which vendors
   - View delivery status
   - Monitor system performance

## 🔌 API Endpoints

### Public Endpoints
```
POST /api/leads/                    # Submit lead
POST /api/vendors/register          # Vendor registration
POST /api/auth/login               # Login
```

### Vendor Endpoints (Requires Auth)
```
GET  /api/vendors/me               # Get profile
GET  /api/vendors/my-leads         # Get assigned leads
POST /api/vendors/buy-credits      # Purchase credits
GET  /api/vendors/payments         # Payment history
```

### Admin Endpoints (Requires Auth)
```
GET  /api/admin/dashboard          # Dashboard stats
GET  /api/admin/vendors            # All vendors
PUT  /api/admin/vendors/:id/credits # Update credits
GET  /api/admin/lead-assignments   # Routing logs
```

### Webhooks
```
POST /api/webhooks/razorpay        # Razorpay webhook
GET  /api/webhooks/payment         # Payment callback
```

## 🎨 Customization

### Adding New Service Types
Edit the service dropdown in `/frontend/templates/forms/lead_form.html`

### Changing Credit Price
Update `CREDIT_PRICE` in `.env` file

### Email Templates
Modify `notification_service.py` for custom email designs

### Dashboard Metrics
Add new metrics in `admin.py` dashboard endpoint

## 🧪 Testing

### Test Lead Submission
```bash
curl -X POST http://localhost:8000/api/leads/ \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "mobile": "9876543210",
    "city": "Surat",
    "service_type": "Solar",
    "budget_range": "1L-2L",
    "notes": "Need solar panels for home"
  }'
```

### Test Vendor Registration
```bash
curl -X POST http://localhost:8000/api/vendors/register \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Solar Pro",
    "owner_name": "Jane Smith",
    "mobile": "9876543211",
    "email": "vendor@example.com",
    "city": "Surat",
    "service_type": "Solar",
    "password": "Vendor@123"
  }'
```

## 📦 Deployment

### Using Docker
```bash
docker build -t lead-vendor-platform .
docker run -p 8000:8000 lead-vendor-platform
```

### Using Heroku
```bash
heroku create lead-vendor-platform
git push heroku main
heroku run python -m alembic upgrade head
```

### Using Railway/Render
- Connect GitHub repository
- Set environment variables
- Deploy automatically

## 🔒 Security Notes

1. **Change Default Admin Password** immediately after first login
2. **Use Strong SECRET_KEY** (32+ characters)
3. **Enable HTTPS** in production
4. **Set CORS** properly for your domain
5. **Secure Database** with strong credentials
6. **Rate Limit** API endpoints
7. **Validate** all user inputs
8. **Log** security events

## 🐛 Troubleshooting

### Database Connection Error
- Check DATABASE_URL in .env
- Ensure PostgreSQL is running (if not using SQLite)

### Lead Not Routing
- Verify vendor has credits
- Check vendor status is ACTIVE
- Confirm city and service type match

### Payment Not Working
- Verify Razorpay credentials
- Check webhook URL is accessible
- Test with demo mode first

### Email Not Sending
- Verify SMTP credentials
- Check Gmail allows less secure apps
- Use app-specific password

## 📞 Support

For issues or questions:
- Create an issue on GitHub
- Email: support@yourcompany.com

## 📄 License

MIT License - feel free to use for commercial projects

## 🙏 Credits

Built with:
- FastAPI
- Tailwind CSS
- Chart.js
- SQLAlchemy
- Razorpay

---

**Made with ❤️ for efficient lead management**
