from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Try to import GinIndex for PostgreSQL, fallback for other databases
try:
    from django.contrib.postgres.indexes import GinIndex
    HAS_POSTGRES = True
except ImportError:
    GinIndex = None
    HAS_POSTGRES = False


# -----------------------------
# Resume Builder Models
# -----------------------------
class ResumeTemplate(models.Model):
    """Template with versioning, configuration and format type"""
    TEMPLATE_FORMATS = [
        ('CLASSIC', 'Classic'),
        ('MODERN', 'Modern'),
        ('CREATIVE', 'Creative'),
        ('TECHNICAL', 'Technical'),
    ]
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    format_type = models.CharField(max_length=20, choices=TEMPLATE_FORMATS)
    thumbnail = models.ImageField(upload_to='resume_templates/', blank=True)
    config = models.JSONField(default=dict, blank=True)
    version = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [GinIndex(fields=['config'])] if HAS_POSTGRES else []
        ordering = ['-version', 'name']

    def __str__(self):
        return f"{self.name} (v{self.version})"


class Resume(models.Model):
    """Central resume model with slug, tags, language and visibility"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='resumes',
        db_index=True
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True)
    summary = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    template = models.ForeignKey(
        ResumeTemplate,
        on_delete=models.SET_NULL,
        null=True,
        related_name='resumes'
    )
    language = models.CharField(max_length=7, default='en')
    visibility = models.CharField(
        max_length=20,
        choices=[('PRIVATE', 'Private'), ('PUBLIC', 'Public'), ('SHARED', 'Shared with Link')],
        default='PRIVATE'
    )
    last_modified = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'title')
        ordering = ['-last_modified']
        indexes = [
            models.Index(fields=['user', 'visibility']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return f"{self.user.email} – {self.title}"


class ResumeSection(models.Model):
    """Flexible sections for custom resume layouts"""
    SECTION_TYPES = [
        ('PERSONAL', 'Personal Information'),
        ('SUMMARY', 'Summary'),
        ('EXPERIENCE', 'Work Experience'),
        ('EDUCATION', 'Education'),
        ('SKILLS', 'Skills'),
        ('PROJECTS', 'Projects'),
        ('CUSTOM', 'Custom Section'),
    ]
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='sections')
    section_type = models.CharField(max_length=20, choices=SECTION_TYPES)
    title = models.CharField(max_length=100)
    content = models.JSONField(default=dict, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        unique_together = ('resume', 'section_type')

    def __str__(self):
        return f"{self.resume.title} – {self.title}"


class WorkExperience(models.Model):
    """Consolidated work experience with achievements and technologies"""
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='work_experiences'
    )
    job_title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    achievements = models.JSONField(default=list, blank=True)
    technologies = models.ManyToManyField('Technology', related_name='experiences', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['company']),
            models.Index(fields=['-start_date']),
        ]

    def __str__(self):
        return f"{self.job_title} at {self.company}"


class TechnicalSkill(models.Model):
    """Link Technology to Resume with proficiency levels"""
    PROGRESS_LEVELS = [
        (20, 'Basic'),
        (40, 'Beginner'),
        (60, 'Intermediate'),
        (80, 'Advanced'),
        (100, 'Expert'),
    ]
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='technical_skills'
    )
    technology = models.ForeignKey(
        'Technology',
        on_delete=models.CASCADE,
        related_name='skill_entries'
    )
    proficiency = models.PositiveIntegerField(
        choices=PROGRESS_LEVELS,
        validators=[MinValueValidator(20), MaxValueValidator(100)]
    )
    years_experience = models.PositiveIntegerField(default=0)
    last_used = models.DateField(null=True, blank=True)
    project_count = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Technical Skill'
        verbose_name_plural = 'Technical Skills'
        unique_together = ('resume', 'technology')
        ordering = ['-proficiency', 'technology__name']
        indexes = [
            models.Index(fields=['proficiency']),
            models.Index(fields=['resume', 'technology']),
        ]

    def __str__(self):
        return f"{self.technology.name} – {self.get_proficiency_display()}"


class Education(models.Model):
    """Validated education entries with date constraints"""
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='educations'
    )
    degree = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    gpa = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(4)]
    )
    description = models.TextField(blank=True)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ['-end_date']
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gte=models.F('start_date')),
                name='education_date_check'
            )
        ]

    def __str__(self):
        return f"{self.degree} from {self.institution}"


class Technology(models.Model):
    """Normalized technology/skill reference"""
    CATEGORIES = [
        ('LANG', 'Programming Language'),
        ('FRAMEWORK', 'Framework'),
        ('TOOL', 'Development Tool'),
        ('CLOUD', 'Cloud Platform'),
        ('DB', 'Database'),
    ]
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    icon = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Technologies'
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"


class Project(models.Model):
    """Enhanced project model with technology M2M"""
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='projects'
    )
    title = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    technologies = models.ManyToManyField(Technology, related_name='projects', blank=True)
    outcomes = models.JSONField(default=dict, blank=True)
    url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-start_date']
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gte=models.F('start_date')),
                name='project_date_check'
            )
        ]

    def __str__(self):
        return f"{self.title} – {self.role}"


class Certification(models.Model):
    """Certification entries linked to technologies"""
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='certifications'
    )
    name = models.CharField(max_length=255)
    issuer = models.CharField(max_length=255)
    issue_date = models.DateField()
    expiration_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=100, blank=True)
    verification_url = models.URLField(blank=True)
    skills = models.ManyToManyField(Technology, related_name='certifications', blank=True)

    class Meta:
        ordering = ['-issue_date']

    def __str__(self):
        return f"{self.name} by {self.issuer}"


class Award(models.Model):
    """Awards and honors linked to resumes"""
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='awards'
    )
    title = models.CharField(max_length=255)
    issuer = models.CharField(max_length=255)
    issue_date = models.DateField()
    category = models.CharField(
        max_length=50,
        choices=[
            ('professional', 'Professional Achievement'),
            ('academic', 'Academic Excellence'),
            ('innovation', 'Innovation'),
        ]
    )
    description = models.TextField(blank=True)
    impact_metrics = models.JSONField(default=dict, blank=True)
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-issue_date']

    def __str__(self):
        return f"{self.title} – {self.issuer}"


class Language(models.Model):
    """Language proficiencies linked to resumes"""
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='languages'
    )
    name = models.CharField(max_length=50)
    proficiency = models.CharField(
        max_length=20,
        choices=[
            ('native', 'Native'),
            ('fluent', 'Fluent'),
            ('professional', 'Professional Working'),
            ('limited', 'Limited Working'),
        ]
    )
    certification = models.CharField(max_length=100, blank=True)
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-proficiency', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_proficiency_display()})"

    def get_proficiency_display(self):
        return self.proficiency
