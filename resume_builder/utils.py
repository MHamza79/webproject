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
        
        # Create custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2c3e50')
        )
        
        section_style = ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=10,
            spaceBefore=20,
            textColor=colors.HexColor('#2c3e50'),
            borderWidth=1,
            borderColor=colors.HexColor('#3498db'),
            borderPadding=5
        )
        
        job_title_style = ParagraphStyle(
            'JobTitle',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=5,
            textColor=colors.HexColor('#34495e'),
            fontName='Helvetica-Bold'
        )
        
        company_style = ParagraphStyle(
            'Company',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=5,
            textColor=colors.HexColor('#7f8c8d'),
            fontName='Helvetica-Oblique'
        )
        
        content_style = ParagraphStyle(
            'Content',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            alignment=TA_JUSTIFY
        )
        
        # Build the story (content)
        story = []
        
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