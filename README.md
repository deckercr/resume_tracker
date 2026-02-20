# 💼 Job Tracker

![Platform](https://img.shields.io/badge/platform-Windows-blue?logo=windows)
![Python](https://img.shields.io/badge/python-3.14%2B-yellow?logo=python)
![License](https://img.shields.io/badge/license-MIT-green)
![Release](https://img.shields.io/github/v/release/deckercr/resume_tracker?label=latest%20release)

A **Windows desktop application** for tracking job applications throughout your job search. Built with Python + pywebview — runs as a native window, no browser required.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📋 **Application Tracking** | Log every job you apply to with company, position, location, salary, contact info, and notes |
| 🏷️ **Status Badges** | Color-coded status tracking: Applied, Screening, Interview, Offer, Rejected, Withdrawn |
| 🔍 **Status Filtering** | Filter your application list by status at a glance |
| 📝 **Job Descriptions** | Save the full job posting text alongside each application |
| 📄 **Resume Manager** | Upload, store, and link PDF or DOCX resumes to individual applications |
| 🔄 **Format Conversion** | Convert resumes between PDF and DOCX right inside the app |
| 📊 **Excel Export** | Export all applications and job descriptions to a `.xlsx` spreadsheet |
| 💾 **Local Storage** | All data is stored locally in a SQLite database — no accounts, no cloud |

---

## ⬇️ Download (Recommended)

**No Python required.** Just download and run.

1. Go to the [**Releases page**](https://github.com/deckercr/resume_tracker/releases/latest)
2. Under **Assets**, download `JobTracker.exe`
3. Double-click `JobTracker.exe` to launch — no installation needed

> **Note:** Windows may show a SmartScreen warning the first time you run it since the executable is not code-signed. Click **"More info" → "Run anyway"** to proceed.

The database (`job_tracker.db`) is created automatically next to the `.exe` on first launch.

---

## 🚀 Usage

### Application List
- The main screen shows all your applications in a sortable table
- Use the **Filter by status** dropdown to narrow the list
- Click **View** to see full details, **Edit** to modify, or **Delete** to remove

### Adding an Application
1. Click **+ New Application** in the top-right or navbar
2. Fill in Company and Position (required), plus any optional fields
3. Click **Add Application** to save

### Job Descriptions
- From an application's detail view, click **Job Description**
- Paste or type the full job posting text and click **Save**
- A green ✅ badge appears on the button when a description is saved

### Resume Manager
- Click **Resumes** in the navbar to open the resume library
- Click **+ Upload Resume**, give it a name, then select a PDF or DOCX file
- From any application's detail view, click **Resume** to link one of your uploaded resumes
- Use **Convert to PDF** or **Convert to DOCX** to generate both formats from a single upload

### Export to Excel
- Click **Export Excel** in the navbar
- Choose a save location — the file contains two sheets: **Applications** and **Job Descriptions**

---

## 🔨 Build It Yourself

You will need **Windows** and **Python 3.14+** with pip.

### Option 1 — Automated (Recommended)

Run the included build script. It installs all dependencies, builds the executable, and optionally cleans up afterward.

```bat
build_win64.bat
```

The finished executable will be at:
```
build\win64\JobTracker.exe
```

### Option 2 — Manual

**1. Clone the repository**
```bash
git clone https://github.com/deckercr/resume_tracker.git
cd resume_tracker
```

**2. Create and activate a virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
pip install pyinstaller PyQt5 PyQtWebEngine qtpy bottle proxy_tools
pip install pywebview --no-deps
```

**4. Build the executable**
```bash
python -m PyInstaller --clean --distpath build\win64 --workpath build\tmp job_tracker.spec
```

Output: `build\win64\JobTracker.exe`

---

## 🐍 Run from Source

If you prefer to run the app directly with Python (no build step):

**1. Clone and enter the repo**
```bash
git clone https://github.com/deckercr/resume_tracker.git
cd resume_tracker
```

**2. Create and activate a virtual environment**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run**
```bash
python app.py
```

A native window will open. The database (`job_tracker.db`) is created automatically in the project directory.

---

## 🗂️ Project Structure

```
job-tracker/
├── app.py              # Entry point — pywebview window, API class
├── models.py           # SQLAlchemy models (applications, job descriptions, resumes)
├── export.py           # Excel export logic
├── requirements.txt    # Python dependencies
├── job_tracker.spec    # PyInstaller build spec
├── build_win64.bat     # Windows build automation script
└── assets/
    ├── index.html      # Single-page UI
    ├── style.css       # Custom styles
    ├── app.js          # Frontend logic and view routing
    └── bootstrap/      # Bootstrap 5.3.3 (bundled locally)
```

---

## 🛠️ Tech Stack

- **[pywebview](https://pywebview.flowrl.com/)** — Native desktop window rendering HTML/CSS/JS
- **[SQLAlchemy](https://www.sqlalchemy.org/)** — SQLite ORM
- **[openpyxl](https://openpyxl.readthedocs.io/)** — Excel export
- **[python-docx](https://python-docx.readthedocs.io/)** — DOCX file handling
- **[fpdf2](https://py-fpdf2.readthedocs.io/)** — PDF generation
- **[PyMuPDF](https://pymupdf.readthedocs.io/)** — PDF text extraction
- **[Bootstrap 5.3.3](https://getbootstrap.com/)** — UI framework (bundled, no CDN)
- **[PyInstaller](https://pyinstaller.org/)** — Windows executable packaging
