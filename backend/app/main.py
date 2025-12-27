from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base, SessionLocal
from .api import auth, leads, vendor, admin, webhooks
from .models import user, vendor as vendor_model, lead, lead_assignment, payment
from .services.auth_service import AuthService
from .models.user import UserRole
from .config import settings

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Lead-Vendor Automation Platform API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Templates
templates = Jinja2Templates(directory="frontend/templates")

# Include routers
app.include_router(auth.router)
app.include_router(leads.router)
app.include_router(vendor.router)
app.include_router(admin.router)
app.include_router(webhooks.router)

# Initialize admin user
@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    try:
        # Check if admin exists
        admin_user = db.query(user.User).filter(
            user.User.email == settings.ADMIN_EMAIL
        ).first()
        
        if not admin_user:
            # Create admin user
            AuthService.create_user(
                db,
                email=settings.ADMIN_EMAIL,
                password=settings.ADMIN_PASSWORD,
                role=UserRole.ADMIN
            )
            print(f"Admin user created: {settings.ADMIN_EMAIL}")
        else:
            print("Admin user already exists")
    finally:
        db.close()

# Frontend routes
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Home page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/lead-form", response_class=HTMLResponse)
async def lead_form(request: Request):
    """Public lead submission form"""
    return templates.TemplateResponse("forms/lead_form.html", {"request": request})

@app.get("/vendor-registration", response_class=HTMLResponse)
async def vendor_registration(request: Request):
    """Public vendor registration form"""
    return templates.TemplateResponse("forms/vendor_registration.html", {"request": request})

@app.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    """Admin dashboard"""
    return templates.TemplateResponse("admin/dashboard.html", {"request": request})

@app.get("/vendor/dashboard", response_class=HTMLResponse)
async def vendor_dashboard(request: Request):
    """Vendor dashboard"""
    return templates.TemplateResponse("vendor/dashboard.html", {"request": request})

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
