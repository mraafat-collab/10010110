import os
import shutil
import uuid
from typing import List, Optional
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy import JSON, Column, Float, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# ---------------------------------------------------------------------------
# 1. DATABASE CONFIGURATION
# ---------------------------------------------------------------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///./hr_system.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------
# 2. SQLALCHEMY MODELS
# ---------------------------------------------------------------------------
class NewHire(Base):
    __tablename__ = "new_hires"

    id = Column(Integer, primary_key=True, index=True)
    photo_url = Column(
        String,
        default="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150",
    )
    employee_name = Column(String, nullable=False)
    branch = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    hiring_date = Column(String, nullable=False)
    grading_system = Column(String, default="Grade 3 - Senior Specialist")
    net_basic_salary = Column(Float, default=0.0)
    net_allowance = Column(Float, default=0.0)
    net_kpi = Column(Float, default=0.0)
    total_net = Column(Float, default=0.0)
    education = Column(String, default="Bachelor's Degree")
    age = Column(Integer, default=30)
    address = Column(String, default="Cairo, Egypt")
    experience = Column(String, default="5 Years")
    manager = Column(String, nullable=False)
    status = Column(String, default="Pending")
    manager_comment = Column(
        String, default="Pending initial onboarding review."
    )
    onboarding_checklist = Column(
        JSON,
        default=lambda: [
            {"id": 1, "label": "ID & Legal Documents Verified", "done": False},
            {"id": 2, "label": "Work Laptop & Access Granted", "done": False},
            {"id": 3, "label": "Signed Contract Uploaded", "done": False},
            {"id": 4, "label": "Bank Account Setup", "done": False},
            {"id": 5, "label": "Medical Insurance Registered", "done": False},
            {"id": 6, "label": "Orientation Scheduled", "done": False},
        ],
    )


class Resignation(Base):
    __tablename__ = "resignations"

    id = Column(Integer, primary_key=True, index=True)
    photo_url = Column(
        String,
        default="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150",
    )
    employee_name = Column(String, nullable=False)
    branch = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    hiring_date = Column(String, nullable=False)
    resignation_date = Column(String, nullable=False)
    last_working_day = Column(String, nullable=False)
    grading = Column(String, default="Grade 4 - Team Lead")
    total_net = Column(Float, default=0.0)
    reason = Column(String, default="Career Advancement")
    notice_status = Column(String, default="30 Days - In Progress")
    handover_status = Column(String, default="Pending Handover Sign-off")
    total_experience = Column(String, default="3 Years, 2 Months")
    manager = Column(String, nullable=False)
    absence = Column(String, default="2 Days Remaining")
    loan_balance = Column(Float, default=0.0)
    status = Column(String, default="Pending")
    manager_comment = Column(String, default="Awaiting exit interview.")


Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------------------------
# 3. PYDANTIC SCHEMAS
# ---------------------------------------------------------------------------
class ChecklistItem(BaseModel):
    id: int
    label: str
    done: bool


class NewHireBase(BaseModel):
    employee_name: str
    branch: str
    job_title: str
    hiring_date: str
    grading_system: Optional[str] = "Grade 3 - Senior Specialist"
    net_basic_salary: float = 0.0
    net_allowance: float = 0.0
    net_kpi: float = 0.0
    total_net: float = 0.0
    education: Optional[str] = "Bachelor's Degree"
    age: Optional[int] = 30
    address: Optional[str] = "Cairo, Egypt"
    experience: Optional[str] = "5 Years"
    manager: str
    status: Optional[str] = "Pending"
    manager_comment: Optional[str] = "Pending initial onboarding review."
    photo_url: Optional[str] = (
        "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150"
    )
    onboarding_checklist: Optional[List[ChecklistItem]] = []


class NewHireCreate(NewHireBase):
    pass


class NewHireResponse(NewHireBase):
    id: int

    class Config:
        from_attributes = True


class ResignationBase(BaseModel):
    employee_name: str
    branch: str
    job_title: str
    hiring_date: str
    resignation_date: str
    last_working_day: str
    grading: Optional[str] = "Grade 4 - Team Lead"
    total_net: float = 0.0
    reason: str
    notice_status: Optional[str] = "30 Days - Active"
    handover_status: Optional[str] = "Pending"
    total_experience: Optional[str] = "2 Years"
    manager: str
    absence: Optional[str] = "0 Days"
    loan_balance: Optional[float] = 0.0
    status: Optional[str] = "Pending"
    manager_comment: Optional[str] = "Pending Manager Review"
    photo_url: Optional[str] = (
        "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150"
    )


class ResignationCreate(ResignationBase):
    pass


class ResignationResponse(ResignationBase):
    id: int

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# 4. FASTAPI APP & ENDPOINTS
# ---------------------------------------------------------------------------
app = FastAPI(title="HR Management System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


# --- Serves index.html at root ---
@app.get("/", response_class=FileResponse)
def read_root():
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    return {"message": "HR API is running. index.html not found."}


# --- API Routes ---
@app.post(
    "/api/hires",
    response_model=NewHireResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_hire(hire: NewHireCreate, db: Session = Depends(get_db)):
    if hire.total_net == 0.0:
        hire.total_net = (
            hire.net_basic_salary + hire.net_allowance + hire.net_kpi
        )

    db_hire = NewHire(**hire.model_dump())
    db.add(db_hire)
    db.commit()
    db.refresh(db_hire)
    return db_hire


@app.get("/api/hires", response_model=List[NewHireResponse])
def get_hires(db: Session = Depends(get_db)):
    return db.query(NewHire).all()


@app.post(
    "/api/resignations",
    response_model=ResignationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_resignation(
    resignation: ResignationCreate, db: Session = Depends(get_db)
):
    db_res = Resignation(**resignation.model_dump())
    db.add(db_res)
    db.commit()
    db.refresh(db_res)
    return db_res


@app.get("/api/resignations", response_model=List[ResignationResponse])
def get_resignations(db: Session = Depends(get_db)):
    return db.query(Resignation).all()
