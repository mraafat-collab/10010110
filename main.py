import os
import pandas as pd
import streamlit as st
from sqlalchemy import (
    JSON,
    Column,
    Float,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker

# ---------------------------------------------------------------------------
# 1. DATABASE CONFIGURATION (SQLite)
# ---------------------------------------------------------------------------
DATABASE_URL = "sqlite:///./hr_system.db"
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class NewHire(Base):
    __tablename__ = "new_hires"

    id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String, nullable=False)
    branch = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    hiring_date = Column(String, nullable=False)
    total_net = Column(Float, default=0.0)
    manager = Column(String, nullable=False)
    status = Column(String, default="Pending")


class Resignation(Base):
    __tablename__ = "resignations"

    id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String, nullable=False)
    branch = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    resignation_date = Column(String, nullable=False)
    last_working_day = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    manager = Column(String, nullable=False)
    status = Column(String, default="Pending")


Base.metadata.create_all(bind=engine)

# ---------------------------------------------------------------------------
# 2. STREAMLIT UI CONFIGURATION
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="HR Management System", page_icon="🏢", layout="wide"
)

# Custom Styling (Dark Brown & Cream Palette)
st.markdown(
    """
    <style>
    .main-title { color: #6B4226; font-weight: bold; }
    .stButton>button { background-color: #6B4226; color: white; border-radius: 6px; font-weight: bold; }
    .stButton>button:hover { background-color: #52321c; color: white; }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🏢 نظام إدارة الموظفين | HR Management System")
st.write("منصة إدارة تعيينات الموظفين الجدد وطلبات الاستقالة")
st.divider()

# Navigation Tabs
tab_hires, tab_resignations, tab_dashboard = st.tabs(
    ["📝 طلبات التعيين", "📄 طلبات الاستقالة", "📊 لوحة البيانات"]
)

# ---------------------------------------------------------------------------
# TAB 1: NEW HIRES FORM
# ---------------------------------------------------------------------------
with tab_hires:
    st.subheader("إضافة طلب تعيين جديد")
    with st.form("hire_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("اسم الموظف *")
            branch = st.text_input("الفرع *")
            job_title = st.text_input("المسمى الوظيفي *")
        with col2:
            hiring_date = st.date_input("تاريخ التعيين")
            total_net = st.number_input(
                "إجمالي الراتب (EGP)", min_value=0.0, value=15000.0
            )
            manager = st.text_input("المدير المباشر *")

        submitted = st.form_submit_button("إرسال طلب التعيين")

        if submitted:
            if name and branch and job_title and manager:
                db = SessionLocal()
                new_entry = NewHire(
                    employee_name=name,
                    branch=branch,
                    job_title=job_title,
                    hiring_date=str(hiring_date),
                    total_net=total_net,
                    manager=manager,
                    status="Pending",
                )
                db.add(new_entry)
                db.commit()
                db.close()
                st.success("تم حفظ طلب التعيين بنجاح!")
            else:
                st.error("يرجى إدخال جميع البيانات المطلوبة (*).")

# ---------------------------------------------------------------------------
# TAB 2: RESIGNATION FORM
# ---------------------------------------------------------------------------
with tab_resignations:
    st.subheader("إضافة طلب استقالة")
    with st.form("resignation_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            r_name = st.text_input("اسم الموظف المستقيل *")
            r_branch = st.text_input("الفرع *")
            r_title = st.text_input("المسمى الوظيفي *")
            r_manager = st.text_input("المدير المباشر *")
        with col2:
            r_date = st.date_input("تاريخ تقديم الاستقالة")
            r_last_day = st.date_input("آخر يوم عمل")
            r_reason = st.text_area("سبب الاستقالة *")

        r_submitted = st.form_submit_button("إرسال طلب الاستقالة")

        if r_submitted:
            if r_name and r_branch and r_title and r_reason and r_manager:
                db = SessionLocal()
                res_entry = Resignation(
                    employee_name=r_name,
                    branch=r_branch,
                    job_title=r_title,
                    resignation_date=str(r_date),
                    last_working_day=str(r_last_day),
                    reason=r_reason,
                    manager=r_manager,
                    status="Pending",
                )
                db.add(res_entry)
                db.commit()
                db.close()
                st.success("تم تسجيل طلب الاستقالة بنجاح!")
            else:
                st.error("يرجى ملء كافة الحقول الأساسية (*).")

# ---------------------------------------------------------------------------
# TAB 3: DASHBOARD / RECORDS VIEW
# ---------------------------------------------------------------------------
with tab_dashboard:
    st.subheader("عرض وحالة السجلات المسجلة")
    db = SessionLocal()

    # Query New Hires
    hires_data = db.query(NewHire).all()
    if hires_data:
        st.markdown("#### 🔹 قائمة التعيينات الجديدة")
        df_hires = pd.DataFrame([h.__dict__ for h in hires_data]).drop(
            columns=["_sa_instance_state"], errors="ignore"
        )
        st.dataframe(df_hires, use_container_width=True, hide_index=True)
    else:
        st.info("لا توجد طلبات تعيين مسجلة.")

    st.divider()

    # Query Resignations
    res_data = db.query(Resignation).all()
    if res_data:
        st.markdown("#### 🔸 قائمة طلبات الاستقالة")
        df_res = pd.DataFrame([r.__dict__ for r in res_data]).drop(
            columns=["_sa_instance_state"], errors="ignore"
        )
        st.dataframe(df_res, use_container_width=True, hide_index=True)
    else:
        st.info("لا توجد طلبات استقالة مسجلة.")

    db.close()
