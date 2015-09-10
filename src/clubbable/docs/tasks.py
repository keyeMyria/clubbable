# -*- coding: utf-8 -*-
"""
Celery tasks.

Start the Celery worker with ::
    $ celery -A clubbable worker -l info

"""
from __future__ import unicode_literals, absolute_import
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from celery import shared_task
from club.models import Member
from django.conf import settings
from django.template import loader
from django.template.context import Context
from docs.models import MessageTemplate


def _render_string(string, context):
    return loader.get_template_from_string(string).render(context)


def _attach_doc(message, doc):
    attachment = MIMEApplication(doc.data)
    attachment.add_header(
        'Content-Disposition', 'attachment', filename=doc.filename)
    message.attach(attachment)


def _attach_text_template(message, template, context, subtype='plain'):
    text = _render_string(template, context)
    part = MIMEText(text, subtype)
    message.attach(part)


def _build_message(template, member):
    context = Context({
        'full_name': member.get_full_name(),
        'formal_name': member.get_formal_name(),
        'docs': ['%s' % a for a in template.docs]
    })
    if template.html:
        message = MIMEMultipart('alternative')
        _attach_text_template(message, template.text, context)
        _attach_text_template(message, template.html, context, 'html')
        for doc in template.docs:
            _attach_doc(message, doc)
    elif template.docs:
        message = MIMEMultipart()
        _attach_text_template(message, template.text, context)
        for doc in template.docs:
            _attach_doc(message, doc)
    else:
        text = _render_string(template.text, context)
        message = MIMEText(text)
    message['To'] = member.email
    message['From'] = settings.FROM_ADDRESS
    message['Subject'] = _render_string(template.subject, context)
    if settings.REPLY_TO_ADDRESS:
        message['Reply-To'] = settings.REPLY_TO_ADDRESS
    if settings.BOUNCE_ADDRESS:
        message['Return-Path'] = settings.BOUNCE_ADDRESS
    return message


@shared_task
def send_message(template_id, member_id):
    template = MessageTemplate.objects.get(template_id)
    member = Member.objects.get(member_id)
    message = _build_message(template, member)
    smtp = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
    smtp.sendmail(settings.FROM_ADDRESS, [member.email], message.as_string())
    smtp.quit()
