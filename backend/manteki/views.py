from django.shortcuts import render, get_object_or_404,redirect
from .models import JobPosting, Application
from django.contrib.auth.decorators import login_required
from .forms import InterviewForm
from .forms import EmployeeDocumentForm
from .models import EmployeeDocument






# Create your views here.

def job_list(request):
    jobs = JobPosting.objects.filter(status='open')
    return render(request, 'manteki/job_list.html', {'jobs': jobs})

def job_detail(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id, status='open')
    return render(request, 'manteki/job_detail.html', {'job': job})
from .forms import ApplicantForm, ApplicationForm

def apply_to_job(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id, status='open')

    if request.method == 'POST':
        applicant_form = ApplicantForm(request.POST)
        application_form = ApplicationForm(request.POST, request.FILES)

        if applicant_form.is_valid() and application_form.is_valid():
            applicant = applicant_form.save()
            application = application_form.save(commit=False)
            application.applicant = applicant
            application.job = job
            application.save()
            notify_applicant(
               application,
               'Application Received',
                f"Hi {application.applicant.full_name}, we've received your application for {job.title}. We'll be in touch soon!"
           )
            return render(request, 'manteki/application_success.html')
    else:
        applicant_form = ApplicantForm()
        application_form = ApplicationForm()

    return render(request, 'manteki/apply.html', {
        'job': job,
        'applicant_form': applicant_form,
        'application_form': application_form,
    })

@login_required
def track_applications(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id)
    applications = Application.objects.filter(job=job)

    if request.method == 'POST':
        app_id = request.POST.get('application_id')
        new_status = request.POST.get('status')
        application = get_object_or_404(Application, id=app_id, job=job)
        application.status = new_status
        application.save()
        if new_status == 'offered':
           notify_applicant(
             application,
             'Job Offer',
             f"Hi {application.applicant.full_name}, congratulations! We're pleased to offer you the position of {application.job.title}. We'll follow up shortly with your offer letter."
            )
        elif new_status == 'hired':
            notify_applicant(
               application,
               'Welcome to the Team',
               f"Hi {application.applicant.full_name}, welcome aboard! We're excited to have you join us as {application.job.title}."
            )
        return redirect('manteki:track_applications', job_id=job.id)

    return render(request, 'manteki/track_applications.html', {
        'job': job,
        'applications': applications,
    })    

@login_required
def schedule_interview(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.application = application
            interview.save()
            application.status = 'interview'
            application.save()
            notify_applicant(
              application,
              'Interview Scheduled',
               f"Hi {application.applicant.full_name}, your interview for {application.job.title} has been scheduled for {interview.scheduled_date}. We look forward to speaking with you!"
            )
            return redirect('manteki:track_applications', job_id=application.job.id)
    else:
        form = InterviewForm()

    return render(request, 'manteki/schedule_interview.html', {
        'application': application,
        'form': form,
    })    
    
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML

@login_required
def generate_offer_letter(request, application_id):
    application = get_object_or_404(Application, id=application_id, status='offered')

    html_string = render_to_string('manteki/offer_letter.html', {
        'application': application,
    })

    pdf = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="offer_letter_{application.applicant.full_name}.pdf"'
    return response    

from django.core.mail import send_mail

def notify_applicant(application, subject, message):
    send_mail(
        subject,
        message,
        None,  # uses DEFAULT_FROM_EMAIL
        [application.applicant.email],
        fail_silently=False,
    )

@login_required
def upload_employee_document(request):
    if request.method == 'POST':
        form = EmployeeDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manteki:employee_documents')
    else:
        form = EmployeeDocumentForm()

    return render(request, 'manteki/upload_employee_document.html', {'form': form})

@login_required
def employee_documents(request):
    documents = EmployeeDocument.objects.all()
    return render(request, 'manteki/employee_documents.html', {'documents': documents})   
