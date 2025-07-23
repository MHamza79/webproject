import os
from django.conf import settings
from django.template.loader import render_to_string
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import logging
from io import BytesIO

logger = logging.getLogger(__name__)

def generate_resume_pdf(resume, context_data=None):
    """
    Generate a PDF from a resume using ReportLab.
    
    Args:
        resume: Resume object
        context_data: Additional context data (optional)
    
    Returns:
        bytes: PDF content as bytes
    """
    try:
        # Create a BytesIO buffer to store the PDF
        buffer = BytesIO()
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # --- Template Selection ---
        template_type = None
        if hasattr(resume, 'template') and resume.template:
            # If using ResumeTemplate FK
            if hasattr(resume.template, 'format_type'):
                template_type = resume.template.format_type.upper()
            else:
                # If using string field
                template_type = str(resume.template).upper()
        else:
            template_type = 'CLASSIC'

        # --- Styles for Each Template ---
        if template_type == 'MODERN':
            # Modern Creative: color accents, two-column, icons
            title_style = ParagraphStyle(
                'ModernTitle', parent=styles['Heading1'], fontSize=26, spaceAfter=18, alignment=TA_CENTER,
                textColor=colors.HexColor('#6C63FF'), fontName='Helvetica-Bold')
            section_style = ParagraphStyle(
                'ModernSection', parent=styles['Heading2'], fontSize=16, spaceAfter=8, spaceBefore=18,
                textColor=colors.HexColor('#6C63FF'), borderWidth=0, fontName='Helvetica-Bold')
            job_title_style = ParagraphStyle(
                'ModernJobTitle', parent=styles['Normal'], fontSize=12, spaceAfter=2, textColor=colors.HexColor('#22223B'), fontName='Helvetica-Bold')
            company_style = ParagraphStyle(
                'ModernCompany', parent=styles['Normal'], fontSize=10, spaceAfter=2, textColor=colors.HexColor('#9A8C98'), fontName='Helvetica-Oblique')
            content_style = ParagraphStyle(
                'ModernContent', parent=styles['Normal'], fontSize=10, spaceAfter=6, alignment=TA_JUSTIFY)
            contact_style = ParagraphStyle(
                'ModernContact', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor('#6C63FF'), alignment=TA_CENTER, spaceAfter=14, leading=15)
        elif template_type == 'TECHNICAL':
            # Technical Specialist: sidebar for contact/skills, main for experience/projects
            title_style = ParagraphStyle(
                'TechTitle', parent=styles['Heading1'], fontSize=24, spaceAfter=16, alignment=TA_CENTER,
                textColor=colors.HexColor('#0077B6'), fontName='Helvetica-Bold')
            section_style = ParagraphStyle(
                'TechSection', parent=styles['Heading2'], fontSize=15, spaceAfter=7, spaceBefore=15,
                textColor=colors.HexColor('#0077B6'), borderWidth=0, fontName='Helvetica-Bold')
            job_title_style = ParagraphStyle(
                'TechJobTitle', parent=styles['Normal'], fontSize=12, spaceAfter=2, textColor=colors.HexColor('#023E8A'), fontName='Helvetica-Bold')
            company_style = ParagraphStyle(
                'TechCompany', parent=styles['Normal'], fontSize=10, spaceAfter=2, textColor=colors.HexColor('#90E0EF'), fontName='Helvetica-Oblique')
            content_style = ParagraphStyle(
                'TechContent', parent=styles['Normal'], fontSize=10, spaceAfter=6, alignment=TA_JUSTIFY)
            contact_style = ParagraphStyle(
                'TechContact', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor('#0077B6'), alignment=TA_CENTER, spaceAfter=14, leading=15)
        else:
            # Classic Professional: clean, blue/gray, single-column
            title_style = ParagraphStyle(
                'ClassicTitle', parent=styles['Heading1'], fontSize=24, spaceAfter=20, alignment=TA_CENTER,
                textColor=colors.HexColor('#2c3e50'))
            section_style = ParagraphStyle(
                'ClassicSection', parent=styles['Heading2'], fontSize=16, spaceAfter=10, spaceBefore=20,
                textColor=colors.HexColor('#2c3e50'), borderWidth=1, borderColor=colors.HexColor('#3498db'), borderPadding=5)
            job_title_style = ParagraphStyle(
                'ClassicJobTitle', parent=styles['Normal'], fontSize=12, spaceAfter=5, textColor=colors.HexColor('#34495e'), fontName='Helvetica-Bold')
            company_style = ParagraphStyle(
                'ClassicCompany', parent=styles['Normal'], fontSize=10, spaceAfter=5, textColor=colors.HexColor('#7f8c8d'), fontName='Helvetica-Oblique')
            content_style = ParagraphStyle(
                'ClassicContent', parent=styles['Normal'], fontSize=10, spaceAfter=8, alignment=TA_JUSTIFY)
            contact_style = ParagraphStyle(
                'ClassicContact', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor('#2c3e50'), alignment=TA_CENTER, spaceAfter=16, leading=15)

        # Build the story (content)
        story = []
        
        # Contact Info Section (improved)
        user = resume.user
        contact_lines = []
        # Name
        name = ''
        if hasattr(user, 'get_full_name') and user.get_full_name():
            name = user.get_full_name()
        elif hasattr(user, 'first_name') or hasattr(user, 'last_name'):
            name = f"{getattr(user, 'first_name', '')} {getattr(user, 'last_name', '')}".strip()
        if name:
            contact_lines.append(f"<b>Name:</b> {name}")
        # Professional Email (prefer resume, fallback to user)
        email = getattr(resume, 'professional_email', None) or getattr(user, 'email', None)
        if email:
            contact_lines.append(f"<b>Email:</b> {email}")
        # Phone (prefer resume, fallback to user)
        phone = getattr(resume, 'phone', None) or getattr(user, 'phone', None)
        if phone:
            contact_lines.append(f"<b>Phone:</b> {phone}")
        # Location
        location = getattr(resume, 'location', None)
        if location:
            contact_lines.append(f"<b>Location:</b> {location}")
        # GitHub
        github = getattr(resume, 'github_url', None)
        if github:
            contact_lines.append(f"<b>GitHub:</b> {github}")
        # LinkedIn
        linkedin = getattr(resume, 'linkedin_url', None)
        if linkedin:
            contact_lines.append(f"<b>LinkedIn:</b> {linkedin}")
        if contact_lines:
            contact_info = '<br/>'.join(contact_lines)
            story.append(Paragraph(contact_info, contact_style))
        
        # Title
        story.append(Paragraph(resume.title, title_style))
        story.append(Spacer(1, 20))
        
        # Summary
        if resume.summary:
            story.append(Paragraph("Professional Summary", section_style))
            story.append(Paragraph(resume.summary, content_style))
            story.append(Spacer(1, 15))
        
        # Work Experience
        work_experiences = resume.work_experiences.all()
        if work_experiences:
            story.append(Paragraph("Work Experience", section_style))
            
            for exp in work_experiences:
                # Job title
                story.append(Paragraph(exp.job_title, job_title_style))
                
                # Company and dates
                date_range = f"{exp.start_date.strftime('%B %Y')} - "
                if exp.is_current:
                    date_range += "Present"
                else:
                    date_range += exp.end_date.strftime('%B %Y')
                
                company_info = f"{exp.company}"
                if exp.location:
                    company_info += f" | {exp.location}"
                company_info += f" | {date_range}"
                
                story.append(Paragraph(company_info, company_style))
                
                # Description
                if exp.description:
                    story.append(Paragraph(exp.description, content_style))
                
                # Achievements
                if exp.achievements:
                    for achievement in exp.achievements:
                        story.append(Paragraph(f"• {achievement}", content_style))
                
                story.append(Spacer(1, 10))
        
        # Education
        educations = resume.educations.all()
        if educations:
            story.append(Paragraph("Education", section_style))
            
            for edu in educations:
                story.append(Paragraph(edu.degree, job_title_style))
                
                edu_info = f"{edu.institution}"
                if edu.location:
                    edu_info += f" | {edu.location}"
                edu_info += f" | {edu.start_date.strftime('%B %Y')} - {edu.end_date.strftime('%B %Y')}"
                if edu.gpa:
                    edu_info += f" | GPA: {edu.gpa}"
                
                story.append(Paragraph(edu_info, company_style))
                
                if edu.description:
                    story.append(Paragraph(edu.description, content_style))
                
                story.append(Spacer(1, 10))
        
        # Technical Skills
        technical_skills = resume.technical_skills.all()
        if technical_skills:
            story.append(Paragraph("Technical Skills", section_style))
            
            skills_text = []
            for skill in technical_skills:
                skill_info = f"{skill.technology.name} ({skill.get_proficiency_display()})"
                if skill.years_experience > 0:
                    skill_info += f" - {skill.years_experience} years"
                skills_text.append(skill_info)
            
            story.append(Paragraph(", ".join(skills_text), content_style))
            story.append(Spacer(1, 15))
        
        # Projects
        projects = resume.projects.all()
        if projects:
            story.append(Paragraph("Projects", section_style))
            
            for project in projects:
                story.append(Paragraph(project.title, job_title_style))
                
                project_info = f"{project.role}"
                if project.start_date:
                    project_info += f" | {project.start_date.strftime('%B %Y')}"
                    if project.end_date:
                        project_info += f" - {project.end_date.strftime('%B %Y')}"
                    else:
                        project_info += " - Ongoing"
                
                story.append(Paragraph(project_info, company_style))
                
                if project.description:
                    story.append(Paragraph(project.description, content_style))
                
                story.append(Spacer(1, 10))
        
        # Certifications
        certifications = resume.certifications.all()
        if certifications:
            story.append(Paragraph("Certifications", section_style))
            
            for cert in certifications:
                story.append(Paragraph(cert.name, job_title_style))
                
                cert_info = f"{cert.issuer} | {cert.issue_date.strftime('%B %Y')}"
                if cert.expiration_date:
                    cert_info += f" | Expires: {cert.expiration_date.strftime('%B %Y')}"
                
                story.append(Paragraph(cert_info, company_style))
                
                if cert.credential_id:
                    story.append(Paragraph(f"Credential ID: {cert.credential_id}", content_style))
                
                story.append(Spacer(1, 10))
        
        # Awards
        awards = resume.awards.all()
        if awards:
            story.append(Paragraph("Awards & Recognition", section_style))
            
            for award in awards:
                story.append(Paragraph(award.title, job_title_style))
                
                award_info = f"{award.issuer} | {award.issue_date.strftime('%B %Y')} | {award.get_category_display()}"
                story.append(Paragraph(award_info, company_style))
                
                if award.description:
                    story.append(Paragraph(award.description, content_style))
                
                story.append(Spacer(1, 10))
        
        # Languages
        languages = resume.languages.all()
        if languages:
            story.append(Paragraph("Languages", section_style))
            
            lang_text = []
            for lang in languages:
                lang_info = f"{lang.name} ({lang.get_proficiency_display()})"
                if lang.certification:
                    lang_info += f" - {lang.certification}"
                lang_text.append(lang_info)
            
            story.append(Paragraph(", ".join(lang_text), content_style))
        
        # Footer
        story.append(Spacer(1, 30))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#7f8c8d')
        )
        story.append(Paragraph("Generated by DiamondTalent Resume Builder", footer_style))
        
        # Build the PDF
        doc.build(story)
        
        # Get the PDF content
        pdf_content = buffer.getvalue()
        buffer.close()
        
        return pdf_content
        
    except Exception as e:
        logger.error(f"Error generating PDF for resume {resume.id}: {str(e)}")
        raise

def get_safe_filename(title):
    """
    Convert a title to a safe filename for PDF download.
    
    Args:
        title: Resume title
    
    Returns:
        str: Safe filename
    """
    import re
    # Remove or replace invalid characters
    safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
    # Limit length
    if len(safe_title) > 50:
        safe_title = safe_title[:50]
    return safe_title.strip() 