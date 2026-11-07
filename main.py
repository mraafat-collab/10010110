import os
import shutil
import uuid
from typing import List, Optional
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy import JSON, Column, Float, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# ---------------------------------------------------------------------------
# 1. DATABASE CONFIGURATION (مدمج بدون الحاجة لملف database.py)
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
# 2. SQLALCHEMY MODELS (النماذج)
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
            {
                "id": 2,
                "label": "Work Laptop & Access Granted",
                "done": False,
            },
            {"id": 3, "label": "Signed Contract Uploaded", "done": False},
            {"id": 4, "label": "Bank Account Setup", "done": False},
            {
                "id": 5,
                "label": "Medical Insurance Registered",
                "done": False,
            },
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


# إنشاء الجداول تلقائياً في قاعدة البيانات
Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------------------------
# 3. PYDANTIC SCHEMAS (المخططات)
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


class NewHireUpdate(BaseModel):
    employee_name: Optional[str] = None
    branch: Optional[str] = None
    job_title: Optional[str] = None
    hiring_date: Optional[str] = None
    grading_system: Optional[str] = None
    net_basic_salary: Optional[float] = None
    net_allowance: Optional[float] = None
    net_kpi: Optional[float] = None
    total_net: Optional[float] = None
    education: Optional[str] = None
    age: Optional[int] = None
    address: Optional[str] = None
    experience: Optional[str] = None
    manager: Optional[str] = None
    status: Optional[str] = None
    manager_comment: Optional[str] = None
    photo_url: Optional[str] = None
    onboarding_checklist: Optional[List[ChecklistItem]] = None


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


class ResignationUpdate(BaseModel):
    employee_name: Optional[str] = None
    branch: Optional[str] = None
    job_title: Optional[str] = None
    hiring_date: Optional[str] = None
    resignation_date: Optional[str] = None
    last_working_day: Optional[str] = None
    grading: Optional[str] = None
    total_net: Optional[float] = None
    reason: Optional[str] = None
    notice_status: Optional[str] = None
    handover_status: Optional[str] = None
    total_experience: Optional[str] = None
    manager: Optional[str] = None
    absence: Optional[str] = None
    loan_balance: Optional[float] = None
    status: Optional[str] = None
    manager_comment: Optional[str] = None
    photo_url: Optional[str] = None


class ResignationResponse(ResignationBase):
    id: int

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# 4. FASTAPI APP & ENDPOINTS (التطبيق والمسارات)
# ---------------------------------------------------------------------------
app = FastAPI(title="HR Management System API", version="1.0.0")

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


# --- رفع الصور ---
@app.post("/api/upload-photo")
async def upload_photo(file: UploadFile = File(...)):
    file_ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"photo_url": f"http://localhost:8000/uploads/{filename}"}


# --- مسارات التعيينات الجديدة (New Hires) ---
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


@app.get("/api/hires/{id}", response_model=NewHireResponse)
def get_hire(id: int, db: Session = Depends(get_db)):
    hire = db.query(NewHire).filter(NewHire.id == id).first()
    if not hire:
        raise HTTPException(
            status_code=404, detail="New hire record not found"
        )
    return hire


@app.put("/api/hires/{id}", response_model=NewHireResponse)
def update_hire(
    id: int, hire_update: NewHireUpdate, db: Session = Depends(get_db)
):
    db_hire = db.query(NewHire).filter(NewHire.id == id).first()
    if not db_hire:
        raise HTTPException(
            status_code=404, detail="New hire record not found"
        )

    update_data = hire_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_hire, key, value)

    db_hire.total_net = (
        db_hire.net_basic_salary + db_hire.net_allowance + db_hire.net_kpi
    )

    db.commit()
    db.refresh(db_hire)
    return db_hire


@app.delete("/api/hires/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hire(id: int, db: Session = Depends(get_db)):
    db_hire = db.query(NewHire).filter(NewHire.id == id).first()
    if not db_hire:
        raise HTTPException(
            status_code=404, detail="New hire record not found"
        )
    db.delete(db_hire)
    db.commit()
    return None


# --- مسارات الاستقالات (Resignations) ---
@app.post(
    "/api/resignations",
    response_model=ResignationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_resignation(
    resignation: ResignationCreate, db: Session = Depends(get_db)
):
    db_resignation = Resignation(**resignation.model_dump())
    db.add(db_resignation)
    db.commit()
    db.refresh(db_resignation)
    return db_resignation


@app.get("/api/resignations", response_model=List[ResignationResponse])
def get_resignations(db: Session = Depends(get_db)):
    return db.query(Resignation).all()


@app.get("/api/resignations/{id}", response_model=ResignationResponse)
def get_resignation(id: int, db: Session = Depends(get_db)):
    res = db.query(Resignation).filter(Resignation.id == id).first()
    if not res:
        raise HTTPException(
            status_code=404, detail="Resignation record not found"
        )
    return res


@app.put("/api/resignations/{id}", response_model=ResignationResponse)
def update_resignation(
    id: int, res_update: ResignationUpdate, db: Session = Depends(get_db)
):
    db_res = db.query(Resignation).filter(Resignation.id == id).first()
    if not db_res:
        raise HTTPException(
            status_code=404, detail="Resignation record not found"
        )

    update_data = res_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_res, key, value)

    db.commit()
    db.refresh(db_res)
    return db_res


@app.delete("/api/resignations/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resignation(id: int, db: Session = Depends(get_db)):
    db_res = db.query(Resignation).filter(Resignation.id == id).first()
    if not db_res:
        raise HTTPException(
            status_code=404, detail="Resignation record not found"
        )
    db.delete(db_res)
    db.commit()
    return None
