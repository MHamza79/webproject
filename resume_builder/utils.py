import os
from django.conf import settings
from django.template.loader import render_to_string
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
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
            # Modern: World-class, Google/Amazon-level professional resume
            doc.leftMargin = doc.rightMargin = doc.topMargin = doc.bottomMargin = inch
            primary_color = colors.HexColor('#4285F4')  # Google blue
            secondary_color = colors.HexColor('#22223B')
            accent_bar = colors.HexColor('#4285F4')
            section_bg = colors.HexColor('#FCFCFC')    # Very light gray
            divider_color = colors.HexColor('#E0E0E0')
            name_style = ParagraphStyle(
                'ModernName', parent=styles['Heading1'], fontSize=32, spaceAfter=6, alignment=TA_LEFT,
                textColor=secondary_color, fontName='Times-Bold')
            contact_style = ParagraphStyle(
                'ModernContact', parent=styles['Normal'], fontSize=12, textColor=secondary_color, alignment=TA_LEFT, spaceAfter=18, fontName='Times-Roman')
            section_style = ParagraphStyle(
                'ModernSection', parent=styles['Heading2'], fontSize=17, spaceAfter=10, spaceBefore=0,
                textColor=primary_color, fontName='Times-Bold', alignment=TA_LEFT)
            job_title_style = ParagraphStyle(
                'ModernJobTitle', parent=styles['Normal'], fontSize=13, spaceAfter=3, textColor=secondary_color, fontName='Times-Bold')
            company_style = ParagraphStyle(
                'ModernCompany', parent=styles['Normal'], fontSize=11, spaceAfter=2, textColor=primary_color, fontName='Times-Italic')
            content_style = ParagraphStyle(
                'ModernContent', parent=styles['Normal'], fontSize=11, spaceAfter=7, alignment=TA_JUSTIFY, fontName='Times-Roman')
            bullet_style = ParagraphStyle(
                'ModernBullet', parent=styles['Normal'], fontSize=11, leftIndent=16, bulletIndent=8, spaceAfter=4, fontName='Times-Roman')

            # Helper for section with left accent bar and divider
            def section_block(elements):
                from reportlab.platypus import Table, TableStyle, HRFlowable
                tbl = Table(
                    [[elements]],
                    colWidths=[doc.width],
                    style=[
                        ('BACKGROUND', (0,0), (-1,-1), section_bg),
                        ('LEFTPADDING', (0,0), (-1,-1), 24),
                        ('RIGHTPADDING', (0,0), (-1,-1), 18),
                        ('TOPPADDING', (0,0), (-1,-1), 16),
                        ('BOTTOMPADDING', (0,0), (-1,-1), 16),
                        ('LINEBEFORE', (0,0), (0,-1), 6, accent_bar),
                    ]
                )
                return tbl

            story = []
            # Name and Contact Info
            user = resume.user
            name = ''
            if hasattr(user, 'get_full_name') and user.get_full_name():
                name = user.get_full_name()
            elif hasattr(user, 'first_name') or hasattr(user, 'last_name'):
                name = f"{getattr(user, 'first_name', '')} {getattr(user, 'last_name', '')}".strip()
            contact_line = []
            email = getattr(resume, 'professional_email', None) or getattr(user, 'email', None)
            if email:
                contact_line.append(f'<a href="mailto:{email}" color="#22223B">{email}</a>')
            phone = getattr(resume, 'phone', None) or getattr(user, 'phone', None)
            if phone:
                contact_line.append(phone)
            location = getattr(resume, 'location', None)
            if location:
                contact_line.append(location)
            github = getattr(resume, 'github_url', None)
            if github:
                contact_line.append(f'<a href="{github}" color="#22223B">GitHub</a>')
            linkedin = getattr(resume, 'linkedin_url', None)
            if linkedin:
                contact_line.append(f'<a href="{linkedin}" color="#4285F4">LinkedIn</a>')
            contact_str = ' | '.join(contact_line)
            story.append(Paragraph(name, name_style))
            story.append(Spacer(1, 10))  # Extra space between name and contact info
            if contact_str:
                story.append(Paragraph(contact_str, contact_style))
            story.append(HRFlowable(width="100%", color=divider_color, thickness=0.7, spaceBefore=10, spaceAfter=18))

            # Summary
            if resume.summary:
                summary_elements = [Paragraph("Professional Summary", section_style), Paragraph(resume.summary, content_style)]
                story.append(section_block(summary_elements))
                story.append(HRFlowable(width="100%", color=divider_color, thickness=0.7, spaceBefore=18, spaceAfter=18))

            # Work Experience
            work_experiences = resume.work_experiences.all()
            if work_experiences:
                work_elements = [Paragraph("Work Experience", section_style)]
                for exp in work_experiences:
                    work_elements.append(Paragraph(exp.job_title, job_title_style))
                    date_range = f"{exp.start_date.strftime('%b %Y')} - "
                    if exp.is_current:
                        date_range += "Present"
                    else:
                        date_range += exp.end_date.strftime('%b %Y')
                    company_info = f"{exp.company}"
                    if exp.location:
                        company_info += f" | {exp.location}"
                    company_info += f" | {date_range}"
                    work_elements.append(Paragraph(company_info, company_style))
                    if exp.description:
                        work_elements.append(Paragraph(exp.description, content_style))
                    if exp.achievements:
                        for achievement in exp.achievements:
                            work_elements.append(Paragraph(f"• {achievement}", bullet_style))
                story.append(section_block(work_elements))
                story.append(HRFlowable(width="100%", color=divider_color, thickness=0.7, spaceBefore=18, spaceAfter=18))

            # Education
            educations = resume.educations.all()
            if educations:
                edu_elements = [Paragraph("Education", section_style)]
                for edu in educations:
                    edu_elements.append(Paragraph(edu.degree, job_title_style))
                    edu_info = f"{edu.institution}"
                    if edu.location:
                        edu_info += f" | {edu.location}"
                    edu_info += f" | {edu.start_date.strftime('%b %Y')} - {edu.end_date.strftime('%b %Y')}"
                    if edu.gpa:
                        edu_info += f" | GPA: {edu.gpa}"
                    edu_elements.append(Paragraph(edu_info, company_style))
                    if edu.description:
                        edu_elements.append(Paragraph(edu.description, content_style))
                story.append(section_block(edu_elements))
                story.append(HRFlowable(width="100%", color=divider_color, thickness=0.7, spaceBefore=18, spaceAfter=18))

            # Technical Skills
            technical_skills = resume.technical_skills.all()
            if technical_skills:
                skills_elements = [Paragraph("Technical Skills", section_style)]
                for skill in technical_skills:
                    skill_info = f"{skill.technology.name} ({skill.get_proficiency_display()})"
                    if skill.years_experience > 0:
                        skill_info += f" - {skill.years_experience} years"
                    skills_elements.append(Paragraph(f"• {skill_info}", bullet_style))
                story.append(section_block(skills_elements))
                story.append(HRFlowable(width="100%", color=divider_color, thickness=0.7, spaceBefore=18, spaceAfter=18))

            # Projects
            projects = resume.projects.all()
            if projects:
                proj_elements = [Paragraph("Projects", section_style)]
                for project in projects:
                    proj_elements.append(Paragraph(project.title, job_title_style))
                    project_info = f"{project.role}"
                    if project.start_date:
                        project_info += f" | {project.start_date.strftime('%b %Y')}"
                        if project.end_date:
                            project_info += f" - {project.end_date.strftime('%b %Y')}"
                        else:
                            project_info += " - Ongoing"
                    proj_elements.append(Paragraph(project_info, company_style))
                    if project.description:
                        proj_elements.append(Paragraph(project.description, content_style))
                story.append(section_block(proj_elements))
                story.append(HRFlowable(width="100%", color=divider_color, thickness=0.7, spaceBefore=18, spaceAfter=18))

            # Certifications
            certifications = resume.certifications.all()
            if certifications:
                cert_elements = [Paragraph("Certifications", section_style)]
                for cert in certifications:
                    cert_elements.append(Paragraph(cert.name, job_title_style))
                    cert_info = f"{cert.issuer} | {cert.issue_date.strftime('%b %Y')}"
                    if cert.expiration_date:
                        cert_info += f" | Expires: {cert.expiration_date.strftime('%b %Y')}"
                    cert_elements.append(Paragraph(cert_info, company_style))
                    if cert.credential_id:
                        cert_elements.append(Paragraph(f"Credential ID: {cert.credential_id}", content_style))
                story.append(section_block(cert_elements))
                story.append(HRFlowable(width="100%", color=divider_color, thickness=0.7, spaceBefore=18, spaceAfter=18))

            # Awards
            awards = resume.awards.all()
            if awards:
                award_elements = [Paragraph("Awards & Recognition", section_style)]
                for award in awards:
                    award_elements.append(Paragraph(award.title, job_title_style))
                    award_info = f"{award.issuer} | {award.issue_date.strftime('%b %Y')} | {award.get_category_display()}"
                    award_elements.append(Paragraph(award_info, company_style))
                    if award.description:
                        award_elements.append(Paragraph(award.description, content_style))
                story.append(section_block(award_elements))
                story.append(HRFlowable(width="100%", color=divider_color, thickness=0.7, spaceBefore=18, spaceAfter=18))

            # Languages
            languages = resume.languages.all()
            if languages:
                lang_elements = [Paragraph("Languages", section_style)]
                lang_text = []
                for lang in languages:
                    lang_info = f"{lang.name} ({lang.get_proficiency_display()})"
                    if lang.certification:
                        lang_info += f" - {lang.certification}"
                    lang_text.append(lang_info)
                for l in lang_text:
                    lang_elements.append(Paragraph(f"• {l}", bullet_style))
                story.append(section_block(lang_elements))
                story.append(HRFlowable(width="100%", color=divider_color, thickness=0.7, spaceBefore=18, spaceAfter=18))

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
        else:
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