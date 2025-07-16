from django.core.management.base import BaseCommand
from resume_builder.models import Technology

class Command(BaseCommand):
    help = 'Create sample technologies for resume builder'

    def handle(self, *args, **options):
        technologies_data = [
            # Programming Languages
            {'name': 'Python', 'category': 'LANG', 'icon': 'fab fa-python'},
            {'name': 'JavaScript', 'category': 'LANG', 'icon': 'fab fa-js-square'},
            {'name': 'Java', 'category': 'LANG', 'icon': 'fab fa-java'},
            {'name': 'C++', 'category': 'LANG', 'icon': 'fas fa-code'},
            {'name': 'C#', 'category': 'LANG', 'icon': 'fas fa-code'},
            {'name': 'PHP', 'category': 'LANG', 'icon': 'fab fa-php'},
            {'name': 'Ruby', 'category': 'LANG', 'icon': 'fas fa-gem'},
            {'name': 'Go', 'category': 'LANG', 'icon': 'fas fa-code'},
            {'name': 'Rust', 'category': 'LANG', 'icon': 'fas fa-code'},
            {'name': 'Swift', 'category': 'LANG', 'icon': 'fab fa-swift'},
            
            # Frameworks
            {'name': 'Django', 'category': 'FRAMEWORK', 'icon': 'fab fa-python'},
            {'name': 'Flask', 'category': 'FRAMEWORK', 'icon': 'fab fa-python'},
            {'name': 'React', 'category': 'FRAMEWORK', 'icon': 'fab fa-react'},
            {'name': 'Angular', 'category': 'FRAMEWORK', 'icon': 'fab fa-angular'},
            {'name': 'Vue.js', 'category': 'FRAMEWORK', 'icon': 'fab fa-vuejs'},
            {'name': 'Node.js', 'category': 'FRAMEWORK', 'icon': 'fab fa-node-js'},
            {'name': 'Express.js', 'category': 'FRAMEWORK', 'icon': 'fab fa-node-js'},
            {'name': 'Spring Boot', 'category': 'FRAMEWORK', 'icon': 'fab fa-java'},
            {'name': 'Laravel', 'category': 'FRAMEWORK', 'icon': 'fab fa-php'},
            {'name': 'Rails', 'category': 'FRAMEWORK', 'icon': 'fas fa-gem'},
            
            # Development Tools
            {'name': 'Git', 'category': 'TOOL', 'icon': 'fab fa-git-alt'},
            {'name': 'Docker', 'category': 'TOOL', 'icon': 'fab fa-docker'},
            {'name': 'Kubernetes', 'category': 'TOOL', 'icon': 'fab fa-docker'},
            {'name': 'Jenkins', 'category': 'TOOL', 'icon': 'fas fa-cogs'},
            {'name': 'GitHub', 'category': 'TOOL', 'icon': 'fab fa-github'},
            {'name': 'GitLab', 'category': 'TOOL', 'icon': 'fab fa-gitlab'},
            {'name': 'VS Code', 'category': 'TOOL', 'icon': 'fas fa-code'},
            {'name': 'IntelliJ IDEA', 'category': 'TOOL', 'icon': 'fas fa-code'},
            {'name': 'Postman', 'category': 'TOOL', 'icon': 'fas fa-paper-plane'},
            
            # Cloud Platforms
            {'name': 'AWS', 'category': 'CLOUD', 'icon': 'fab fa-aws'},
            {'name': 'Azure', 'category': 'CLOUD', 'icon': 'fab fa-microsoft'},
            {'name': 'Google Cloud', 'category': 'CLOUD', 'icon': 'fab fa-google'},
            {'name': 'Heroku', 'category': 'CLOUD', 'icon': 'fas fa-cloud'},
            {'name': 'DigitalOcean', 'category': 'CLOUD', 'icon': 'fas fa-cloud'},
            
            # Databases
            {'name': 'PostgreSQL', 'category': 'DB', 'icon': 'fas fa-database'},
            {'name': 'MySQL', 'category': 'DB', 'icon': 'fas fa-database'},
            {'name': 'MongoDB', 'category': 'DB', 'icon': 'fas fa-database'},
            {'name': 'Redis', 'category': 'DB', 'icon': 'fas fa-database'},
            {'name': 'SQLite', 'category': 'DB', 'icon': 'fas fa-database'},
            {'name': 'Oracle', 'category': 'DB', 'icon': 'fas fa-database'},
            {'name': 'SQL Server', 'category': 'DB', 'icon': 'fas fa-database'},
        ]

        created_count = 0
        for tech_data in technologies_data:
            technology, created = Technology.objects.get_or_create(
                name=tech_data['name'],
                defaults=tech_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created technology: {technology.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Technology already exists: {technology.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new technologies')
        ) 