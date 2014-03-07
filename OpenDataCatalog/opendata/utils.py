__author__ = 'johnback'

from django.template.loader import render_to_string
from django.core.mail import EmailMessage, mail_managers

from .models import Submission

import simplejson as json


def send_email(user, data):
    """
    Sends an email with a new data submission, and stores the submission as a suggestion
    """
    subject, user_email = 'OpenDataCincy - Data Submission', (user.get_full_name(), user.email)
    text_content = render_to_string('submit_email.txt', data)
    text_content_copy = render_to_string('submit_email_copy.txt', data)

    # mail_managers(subject, text_content)

    msg = EmailMessage(subject, text_content_copy, to=user_email)
    msg.send()

    # Create new user submission object.
    sug_object = Submission()
    sug_object.user = user
    sug_object.email_text = text_content

    # Prep data for serialization
    data['submit_date'] = str(data.get('submit_date', ''))
    data['release_date'] = str(data.get('release_date', ''))

    try:
        sug_object.json_text = json.dumps(data)
    except TypeError as ex:
        print data
        raise TypeError(ex)
        # Something was not consumed by the json serializer..
        # sug_object.json_text = ''

    # Save the submission
    sug_object.save()

    return sug_object
