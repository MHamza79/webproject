import re
import json
from typing import List, Dict, Tuple
from django.conf import settings
from .models import Resume, WorkExperience, TechnicalSkill

class ResumeAnalyzer:
    """AI-powered resume analysis and enhancement service"""
    
    # Common job keywords by industry
    INDUSTRY_KEYWORDS = {
        'technology': [
            'python', 'javascript', 'react', 'node.js', 'aws', 'docker', 'kubernetes',
            'machine learning', 'ai', 'data science', 'sql', 'git', 'agile', 'scrum',
            'microservices', 'api', 'rest', 'graphql', 'devops', 'ci/cd'
        ],
        'finance': [
            'financial modeling', 'excel', 'vba', 'sql', 'risk management', 'portfolio',
            'investment', 'trading', 'derivatives', 'valuation', 'accounting', 'audit',
            'compliance', 'regulatory', 'bloomberg', 'reuters', 'market analysis'
        ],
        'healthcare': [
            'patient care', 'clinical', 'medical', 'healthcare', 'nursing', 'pharmacy',
            'diagnosis', 'treatment', 'medication', 'vital signs', 'electronic health records',
            'hipaa', 'fda', 'clinical trials', 'research', 'public health'
        ],
        'marketing': [
            'digital marketing', 'seo', 'sem', 'social media', 'content marketing',
            'email marketing', 'analytics', 'google analytics', 'facebook ads',
            'brand management', 'campaign', 'lead generation', 'conversion'
        ]
    }
    
    # Action verbs for bullet points
    ACTION_VERBS = [
        'developed', 'implemented', 'managed', 'led', 'created', 'designed',
        'analyzed', 'optimized', 'increased', 'decreased', 'improved', 'streamlined',
        'coordinated', 'facilitated', 'delivered', 'achieved', 'maintained',
        'established', 'built', 'launched', 'executed', 'planned', 'organized'
    ]
    
    def __init__(self, resume: Resume):
        self.resume = resume
        self.content = self._extract_content()
    
    def _extract_content(self) -> str:
        """Extract all text content from resume"""
        content_parts = []
        
        if self.resume.summary:
            content_parts.append(self.resume.summary)
        
        for exp in self.resume.work_experiences.all():
            content_parts.append(f"{exp.job_title} {exp.company} {exp.description}")
        
        for edu in self.resume.educations.all():
            content_parts.append(f"{edu.degree} {edu.institution}")
        
        for skill in self.resume.technical_skills.all():
            tech_name = skill.technology.name if skill.technology else ''
            description = getattr(skill, 'description', '')
            content_parts.append(f"{tech_name} {description}")
        
        for project in self.resume.projects.all():
            content_parts.append(f"{project.title} {project.description}")
        
        return ' '.join(content_parts).lower()
    
    def analyze_ats_score(self) -> int:
        """Calculate ATS (Applicant Tracking System) compatibility score"""
        score = 0
        max_score = 100
        
        # Check for common resume elements
        if self.resume.summary:
            score += 10
        
        if self.resume.work_experiences.exists():
            score += 20
        
        if self.resume.educations.exists():
            score += 15
        
        if self.resume.technical_skills.exists():
            score += 15
        
        # Check for action verbs
        action_verb_count = sum(1 for verb in self.ACTION_VERBS if verb in self.content)
        score += min(action_verb_count * 2, 20)
        
        # Check for quantifiable achievements
        numbers = re.findall(r'\d+', self.content)
        score += min(len(numbers) * 2, 20)
        
        return min(score, max_score)
    
    def suggest_keywords(self, job_title: str = None) -> List[str]:
        """Suggest relevant keywords based on job title or resume content"""
        if job_title:
            job_title_lower = job_title.lower()
            
            # Determine industry from job title
            for industry, keywords in self.INDUSTRY_KEYWORDS.items():
                if any(word in job_title_lower for word in industry.split()):
                    return keywords[:10]  # Return top 10 keywords
        
        # Fallback: analyze content and suggest based on what's missing
        existing_keywords = set(self.content.split())
        all_keywords = set()
        
        for keywords in self.INDUSTRY_KEYWORDS.values():
            all_keywords.update(keywords)
        
        missing_keywords = all_keywords - existing_keywords
        return list(missing_keywords)[:10]
    
    def suggest_bullet_points(self, job_title: str, company: str) -> List[str]:
        """Generate AI-powered bullet point suggestions"""
        suggestions = []
        
        # Template-based suggestions
        templates = [
            f"Developed and maintained {job_title.lower()} solutions that improved efficiency by 25%",
            f"Collaborated with cross-functional teams to deliver {job_title.lower()} projects on time and within budget",
            f"Implemented best practices for {job_title.lower()} that resulted in 30% faster delivery times",
            f"Led {job_title.lower()} initiatives that increased team productivity by 20%",
            f"Created comprehensive documentation for {job_title.lower()} processes and procedures",
            f"Analyzed and optimized {job_title.lower()} workflows, reducing costs by 15%",
            f"Mentored junior team members in {job_title.lower()} best practices and methodologies",
            f"Established quality assurance processes for {job_title.lower()} deliverables",
        ]
        
        return templates[:5]  # Return top 5 suggestions
    
    def get_improvement_suggestions(self) -> List[Dict]:
        """Get comprehensive improvement suggestions"""
        suggestions = []
        
        # Check summary
        if not self.resume.summary:
            suggestions.append({
                'type': 'missing',
                'section': 'summary',
                'message': 'Add a professional summary to make your resume stand out',
                'priority': 'high'
            })
        elif len(self.resume.summary) < 100:
            suggestions.append({
                'type': 'improvement',
                'section': 'summary',
                'message': 'Your summary could be more detailed. Aim for 100-200 words',
                'priority': 'medium'
            })
        
        # Check work experience
        if not self.resume.work_experiences.exists():
            suggestions.append({
                'type': 'missing',
                'section': 'work_experience',
                'message': 'Add work experience to showcase your professional background',
                'priority': 'high'
            })
        
        # Check for action verbs
        action_verb_count = sum(1 for verb in self.ACTION_VERBS if verb in self.content)
        if action_verb_count < 5:
            suggestions.append({
                'type': 'improvement',
                'section': 'content',
                'message': 'Use more action verbs to make your achievements stand out',
                'priority': 'medium'
            })
        
        # Check for quantifiable achievements
        numbers = re.findall(r'\d+', self.content)
        if len(numbers) < 3:
            suggestions.append({
                'type': 'improvement',
                'section': 'content',
                'message': 'Add quantifiable achievements (percentages, numbers) to make your resume more impactful',
                'priority': 'high'
            })
        
        return suggestions
    
    def generate_cover_letter_content(self, job_title: str, company: str) -> str:
        """Generate cover letter content based on resume"""
        template = f"""
Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company}. With my background in {self._get_primary_skill()}, I am confident in my ability to contribute effectively to your team.

{self._generate_cover_letter_body(job_title, company)}

I am particularly drawn to {company} because of its reputation for {self._get_company_highlight()}. I am excited about the opportunity to bring my skills and experience to your organization and contribute to its continued success.

Thank you for considering my application. I look forward to discussing how my background, skills, and enthusiasm can benefit {company}.

Best regards,
{self._get_user_name()}
        """
        
        return template.strip()
    
    def _get_primary_skill(self) -> str:
        """Get primary skill from resume"""
        skills = self.resume.technical_skills.all()
        if skills.exists():
            first_skill = skills.first()
            if first_skill.technology and hasattr(first_skill.technology, 'name'):
                return first_skill.technology.name
        return "professional development"
    
    def _get_user_name(self) -> str:
        """Get user's full name or username"""
        user = self.resume.user
        if hasattr(user, 'get_full_name') and user.get_full_name():
            return user.get_full_name()
        return user.username
    
    def _generate_cover_letter_body(self, job_title: str, company: str) -> str:
        """Generate the main body of cover letter"""
        experiences = self.resume.work_experiences.all()
        if experiences.exists():
            latest_exp = experiences.first()
            return f"In my most recent role as {latest_exp.job_title} at {latest_exp.company}, I {self._get_key_achievement(latest_exp)}. This experience, combined with my {self._get_primary_skill()} skills, positions me well for the {job_title} role."
        
        return f"My background in {self._get_primary_skill()} and passion for {job_title.lower()} make me an ideal candidate for this position."
    
    def _get_key_achievement(self, experience: WorkExperience) -> str:
        """Extract key achievement from work experience"""
        if experience.description:
            # Extract first sentence or first 100 characters
            sentences = experience.description.split('.')
            if sentences:
                return sentences[0][:100] + "..."
        return "gained valuable experience in the field"
    
    def _get_company_highlight(self) -> str:
        """Generate company highlight for cover letter"""
        highlights = [
            "innovation and excellence",
            "professional development and growth",
            "collaborative work environment",
            "industry leadership",
            "commitment to quality"
        ]
        return highlights[0]  # For now, return first option

class ResumeEnhancer:
    """Service for enhancing resume content and formatting"""
    
    @staticmethod
    def optimize_for_ats(resume: Resume) -> Dict:
        """Optimize resume for ATS systems"""
        content = ResumeAnalyzer(resume).content
        
        # Check for common ATS issues
        issues = []
        
        # Check for complex formatting
        if len(content) > 10000:  # Too long
            issues.append("Resume is too long. Consider shortening to 1-2 pages")
        
        # Check for keywords
        keyword_density = ResumeAnalyzer(resume).analyze_ats_score()
        if keyword_density < 70:
            issues.append("Low keyword density. Consider adding more relevant keywords")
        
        # Check for action verbs
        action_verbs = ResumeAnalyzer.ACTION_VERBS
        verb_count = sum(1 for verb in action_verbs if verb in content)
        if verb_count < 5:
            issues.append("Use more action verbs to start bullet points")
        
        return {
            'score': keyword_density,
            'issues': issues,
            'suggestions': ResumeAnalyzer(resume).get_improvement_suggestions()
        }
    
    @staticmethod
    def generate_resume_variations(resume: Resume, job_title: str) -> List[Dict]:
        """Generate different versions of resume for different job applications"""
        variations = []
        
        # Version 1: Skills-focused
        variations.append({
            'name': f"{resume.title} - Skills Focused",
            'description': 'Emphasizes technical skills and certifications',
            'template': 'tech',
            'color_scheme': 'blue'
        })
        
        # Version 2: Experience-focused
        variations.append({
            'name': f"{resume.title} - Experience Focused",
            'description': 'Highlights work experience and achievements',
            'template': 'professional',
            'color_scheme': 'navy'
        })
        
        # Version 3: Creative
        variations.append({
            'name': f"{resume.title} - Creative",
            'description': 'Modern design with visual appeal',
            'template': 'creative',
            'color_scheme': 'purple'
        })
        
        return variations 