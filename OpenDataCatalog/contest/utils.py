from django.template.loader import render_to_string
from django.core.mail import mail_managers, EmailMessage

from datetime import datetime


def process_contest_entry(form):
    data = {
        #"submitter": request.user.username,
        "submit_date": datetime.now(),
        "org_name": form.cleaned_data.get("org_name"),
        "org_url": form.cleaned_data.get("org_url"),
        "contact_person": form.cleaned_data.get("contact_person"),
        "contact_phone": form.cleaned_data.get("contact_phone"),
        "contact_email": form.cleaned_data.get("contact_email"),
        "data_set": form.cleaned_data.get("data_set"),
        "data_use": form.cleaned_data.get("data_use"),
        "data_mission": form.cleaned_data.get("data_mission")
    }

    subject = 'OpenDataCincy - Contest Submission'
    user_email = form.cleaned_data.get("contact_email")
    text_content = render_to_string('contest/submit_email.txt', data)
    text_content_copy = render_to_string('contest/submit_email_copy.txt', data)
    mail_managers(subject, text_content)

    msg = EmailMessage(subject, text_content_copy, to=[user_email])
    return msg.send()
