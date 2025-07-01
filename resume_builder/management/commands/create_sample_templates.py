from django.core.management.base import BaseCommand
from resume_builder.models import ResumeTemplate

class Command(BaseCommand):
    help = 'Create sample resume templates'

    def handle(self, *args, **options):
        templates_data = [
            {
                'name': 'Classic Professional',
                'description': 'A traditional, clean resume template suitable for most industries',
                'format_type': 'CLASSIC',
                'version': 1,
                'is_active': True
            },
            {
                'name': 'Modern Creative',
                'description': 'A contemporary design with visual elements for creative professionals',
                'format_type': 'MODERN',
                'version': 1,
                'is_active': True
            },
            {
                'name': 'Technical Specialist',
                'description': 'Optimized for technical roles with emphasis on skills and projects',
                'format_type': 'TECHNICAL',
                'version': 1,
                'is_active': True
            },
            {
                'name': 'Executive Summary',
                'description': 'Professional template for senior-level positions',
                'format_type': 'CLASSIC',
                'version': 1,
                'is_active': True
            }
        ]

        created_count = 0
        for template_data in templates_data:
            template, created = ResumeTemplate.objects.get_or_create(
                name=template_data['name'],
                defaults=template_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created template: {template.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Template already exists: {template.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new templates')
        ) 