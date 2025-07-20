from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from resume_builder.models import Resume
from resume_builder.utils import generate_resume_pdf, get_safe_filename
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Test PDF generation for resumes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user-email',
            type=str,
            help='Email of the user whose resumes to test',
        )
        parser.add_argument(
            '--output-dir',
            type=str,
            default='test_pdfs',
            help='Directory to save test PDFs',
        )

    def handle(self, *args, **options):
        user_email = options['user_email']
        output_dir = options['output_dir']

        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            self.stdout.write(f"Created output directory: {output_dir}")

        # Get user
        if user_email:
            try:
                user = User.objects.get(email=user_email)
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"User with email {user_email} not found"))
                return
        else:
            # Get the first user with resumes
            user = User.objects.filter(resumes__isnull=False).first()
            if not user:
                self.stdout.write(self.style.ERROR("No users with resumes found"))
                return

        # Get user's resumes
        resumes = Resume.objects.filter(user=user)
        if not resumes.exists():
            self.stdout.write(self.style.ERROR(f"No resumes found for user {user.email}"))
            return

        self.stdout.write(f"Testing PDF generation for user: {user.email}")
        self.stdout.write(f"Found {resumes.count()} resume(s)")

        success_count = 0
        error_count = 0

        for resume in resumes:
            try:
                self.stdout.write(f"Generating PDF for resume: {resume.title}")
                
                # Generate PDF
                pdf_content = generate_resume_pdf(resume)
                
                # Create safe filename
                safe_filename = get_safe_filename(resume.title)
                pdf_path = os.path.join(output_dir, f"{safe_filename}.pdf")
                
                # Save PDF to file
                with open(pdf_path, 'wb') as f:
                    f.write(pdf_content)
                
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Successfully generated: {pdf_path}")
                )
                success_count += 1
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"✗ Error generating PDF for {resume.title}: {str(e)}")
                )
                error_count += 1

        # Summary
        self.stdout.write("\n" + "="*50)
        self.stdout.write("PDF Generation Test Summary:")
        self.stdout.write(f"Total resumes: {resumes.count()}")
        self.stdout.write(f"Successful: {success_count}")
        self.stdout.write(f"Failed: {error_count}")
        self.stdout.write(f"Output directory: {os.path.abspath(output_dir)}")
        
        if success_count > 0:
            self.stdout.write(
                self.style.SUCCESS("PDF generation test completed successfully!")
            )
        else:
            self.stdout.write(
                self.style.ERROR("PDF generation test failed!")
            ) 