# 🚀 Lead-Vendor Automation Platform

Complete lead management and vendor distribution system with automatic ID generation, duplicate detection, and intelligent routing.

## ✨ Features

- 🎯 **Auto ID Generation** - No manual date input required
- 🔍 **Duplicate Detection** - Prevents duplicate leads automatically
- 📱 **Responsive Dashboards** - Works on mobile, tablet, and desktop
- 🤖 **Smart Routing Engine** - Routes leads based on city, service, and budget
- 💳 **Payment Integration** - Razorpay with automatic credit top-up
- 📧 **Multi-channel Notifications** - WhatsApp + Email delivery
- 📊 **Real-time Analytics** - Charts and metrics for admins and vendors

## 🛠️ Tech Stack

**Backend:**
- Python 3.11+
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication

**Frontend:**
- HTML5 + CSS3
- Tailwind CSS
- Chart.js
- Responsive Design

**Integrations:**
- Razorpay/Stripe (Payments)
- WhatsApp API (Notifications)
- SMTP (Email)

## 📋 Prerequisites

- Python 3.11 or higher
- PostgreSQL 13 or higher
- pip (Python package manager)

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/lead-vendor-platform.git
cd lead-vendor-platform
```

### 2. Create Database
```bash
createdb lead_vendor_db
psql -U postgres -d lead_vendor_db -f database/schema.sql
```

### 3. Install Dependencies
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
# Edit .env with your credentials
```

### 5. Run Application
```bash
uvicorn app.main:app --reload
```

Visit: http://localhost:8000

## 📁 Project Structure
