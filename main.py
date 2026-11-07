I want you to build a complete Streamlit application (app.py) for an HR Management System that handles **New Hire Approvals** and **Resignation Approvals**. The app must be fully functional, professional, and production-ready.

---

## 🎨 DESIGN & UI REQUIREMENTS:

The forms must look exactly like professional HR documents with this design system:
- **Primary color**: Dark brown (#6B4226 or similar)
- **Secondary color**: Light beige/cream (#F5EDE0)
- **Accent**: White cards with subtle shadows
- **Font**: Clean, professional (use Streamlit's default or custom CSS)
- **Layout**: Card-based, sectioned, with clear headers

---

## 📄 PAGE 1: NEW HIRE APPROVAL FORM

The form must display:

### Header Section:
- Company name (top-left)
- "New Hire Approval Form" title
- Status badge (PENDING / APPROVED / REJECTED) with colored dot
- "Dear Mr. [Manager Name], Greetings"

### Candidate Profile Card (top-right):
- Candidate photo (upload or placeholder)
- Candidate Name
- Job Title
- Branch

### Key Metrics Row (4 cards):
- Total Net (EGP)
- Hiring Date
- Job Title
- Manager

### Data Table (Field | Value):
Fields to include:
- Employee Name
- Branch
- Job Title
- Hiring Date
- Grading System
- Net Basic Salary EGP
- Net Allowance EGP
- Net KPI's Amount 100% EGP
- Total Net to pay EGP
- Educational Qualifications
- Age
- Address
- Professional Experience
- Direct Manager
- Status
- Manager Comment

### Onboarding Checklist Section:
- Progress bar showing X/6 completed
- 6 checkboxes: Contract signed, Medical/insurance done, System access created, ID & documents collected, Uniform/equipment issued, Orientation completed

### Footer:
- Signature lines: Candidate | Direct Manager | HR

---

## 📄 PAGE 2: RESIGNATION APPROVAL REQUEST

The form must display:

### Header Section:
- "Dear Mr. [Manager Name],"
- "RESIGNATION APPROVAL REQUEST" title

### Employee Profile Card (top-right):
- Employee photo
- Name
- Job Title
- "Resigning [Date]"

### Resignation Journey Timeline (horizontal):
5 steps with icons connected by a line:
1. Joined (date) - person icon
2. Total Experience (days) - trophy icon
3. Resignation Letter Submitted (date) - document icon
4. Notice Period Status - clock icon
5. Resignation Process Finalized Approved (date) - checkmark icon

### Key Metrics Row (4 cards):
- Total Net Pay (EGP)
- Last Working Day
- Reason for Leaving
- Direct Manager

### Data Table (Field | Value):
Fields to include:
- Employee Name
- Branch
- Job Title
- Hiring Date
- Resignation Date
- Last Working Day
- Grading System
- Total Net to pay EGP
- Reason for Leaving
- Notice Period Status
- Handover Status
- Total Experience
- Direct Manager
- Absence during the year
- Loan balance

### Manager Action Items Section:
Title: "Resignation Next Steps"
4 action items with icons:
1. Calculate final dues and payout (calculator icon)
2. Review notice period waiver request (clock icon)
3. Facilitate handover process (handshake icon)
4. Schedule property return (box icon)
5. Issue final acceptance letter and experience certificate (mail icon)

---

## 🗂️ DATA & STORAGE REQUIREMENTS:

1. **File-based storage**: Use JSON files to store all hire and resignation records
   - `data/hires.json` - stores all new hire records
   - `data/resignations.json` - stores all resignation records
   - Create the `data/` folder automatically if it doesn't exist

2. **CRUD Operations**:
   - Add new hire / resignation
   - View existing records
   - Update status (Pending → Approved/Rejected)
   - Delete records

3. **Photo Upload**: Allow uploading employee/candidate photos, save them to `uploads/` folder and display in forms

---

## 🖨️ PRINT & EXPORT REQUIREMENTS:

1. **Print Button**: Each form must have a "Print" button that triggers browser print (use `st.markdown` with JavaScript or `streamlit-print` component)
2. **Save as PNG**: Use `streamlit-image-coordinates` or `html2canvas` approach, or use `imgkit`/`selenium` to capture the form as PNG and offer download
3. **Export to PDF**: Optional - use `fpdf` or `reportlab` to generate PDF

---

## 🧭 APP NAVIGATION (Sidebar):

- 📋 New Hire Approval Form
- 📤 Resignation Approval Request
- 📁 View Saved Records
- ➕ Add New Record
- ⚙️ Settings

---

## 📦 REQUIRED LIBRARIES:
