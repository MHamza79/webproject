# DiamondTalent Resume Builder

## 🚀 Overview

DiamondTalent Resume Builder is a modern, AI-powered web application for creating, analyzing, and exporting professional resumes and cover letters. It features advanced templates, real-time feedback, ATS optimization, and PDF/Word export, all within a beautiful, user-friendly interface.

---

## 🎯 Features

- **AI-Powered Resume Analysis**: Get instant ATS (Applicant Tracking System) compatibility scores, keyword suggestions, and actionable improvement tips.
- **Professional Templates**: Choose from multiple industry-specific, customizable templates with color schemes.
- **Live Preview**: See your resume update in real time as you edit.
- **PDF & Word Export**: Download your resume in high-quality PDF or Word format.
- **Cover Letter Generator**: Instantly generate tailored cover letters based on your resume and job details.
- **Bullet Point Generator**: Get AI-powered suggestions for impactful work experience bullet points.
- **Resume Variations**: Create multiple versions of your resume for different job applications.
- **Dashboard & Progress Tracking**: Visualize your progress and recent activity.
- **User Authentication**: Secure login, registration, and privacy controls.
- **Modern UI/UX**: Responsive, mobile-friendly design using Bootstrap 5.

---

## 🖥️ How to Preview Templates in the Browser

1. **Start the Django Development Server:**
   ```bash
   python manage.py runserver
   ```
2. **Log in** at [http://127.0.0.1:8000/accounts/login/](http://127.0.0.1:8000/accounts/login/)
3. **Navigate to "My Resumes"** from the dashboard or main menu.
4. **Click on a resume** to view its details and see a live preview using the selected template.
   - Example template files:
     - `templates/sample/sample_template.html`
     - `templates/sample/sample2_template.html`
     - `templates/resume_builder/resume_pdf.html` (for PDF rendering)

---

## 📝 How to Render Templates as PDF Using WeasyPrint

> **Note:** The built-in PDF export uses ReportLab, but you can also render any HTML template as a PDF using [WeasyPrint](https://weasyprint.org/).

### 1. Install WeasyPrint
```bash
pip install WeasyPrint
```

### 2. Render a Django Template as PDF (Python Example)
```python
from django.template.loader import render_to_string
from weasyprint import HTML

context = { 'resume': resume, ... }  # Fill with your data
html_string = render_to_string('resume_builder/resume_pdf.html', context)
HTML(string=html_string).write_pdf('output_resume.pdf')
```
- Replace the template path and context as needed.

### 3. Render a Static HTML File as PDF (Command Line)
```bash
weasyprint input.html output.pdf
```

---

## ⚙️ Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd <project-folder>
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
4. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```
5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

---

## 🛠️ Usage Instructions

- **Create an account** or log in.
- **Build your resume** by adding sections: Work Experience, Education, Skills, Projects, Certifications, Awards, Languages, etc.
- **Select a template** and color scheme.
- **Preview your resume** in real time.
- **Analyze your resume** for ATS compatibility and get improvement suggestions.
- **Download as PDF/Word** or generate a cover letter.
- **Create multiple resume versions** for different jobs.

---

## 🧩 Key Technologies
- **Backend:** Django (Python)
- **Frontend:** Bootstrap 5, HTML5, CSS3
- **PDF Generation:** ReportLab (built-in), WeasyPrint (optional)
- **AI/Analysis:** Custom Django services
- **Database:** PostgreSQL (default), SQLite (dev)

---

## 🐞 Troubleshooting
- **PDF/Word Export Issues:** Ensure all dependencies are installed. For WeasyPrint, install system dependencies as per [WeasyPrint docs](https://weasyprint.readthedocs.io/).
- **Static Files Not Loading:** Run `python manage.py collectstatic` if needed.
- **Database Errors:** Check your database settings in `core/settings.py` and ensure migrations are applied.
- **Missing Templates:** Make sure your template paths are correct and templates exist in the `templates/` directory.

---

## 🙏 Credits & Links
- **Project Lead:** DiamondTalent Team
- **UI Template:** NiceAdmin (Bootstrap 5)
- **PDF Engine:** [ReportLab](https://www.reportlab.com/), [WeasyPrint](https://weasyprint.org/)
- **Django:** [https://www.djangoproject.com/](https://www.djangoproject.com/)

---

**Happy resume building!** 