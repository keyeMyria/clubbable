# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
import magic
from docs.models import Document, Folder
from mailer.tasks import send_doc


class DocList(ListView):
    context_object_name = 'docs'

    def get_queryset(self):
        folder = get_object_or_404(Folder, pk=self.args[0])
        return Document.objects.filter(folder=folder)


def send(request, folder_id, pk):
    if request.method == 'POST':
        to = request.POST['to']
        send_doc.delay(
            to=to,
            subject=request.POST['subject'],
            text=request.POST['text'],
            doc_id=pk,
            address=request.user.email if to == 'Myself' else None,
        )
        messages.info(request, 'Your message is queued for sending.')
        return HttpResponseRedirect(reverse('doc_list'))
    doc = get_object_or_404(Document, pk=pk)
    return render(request, 'docs/send_doc.html', {'doc': doc})


def download(request, folder_id, pk, filename):
    doc = get_object_or_404(Document, pk=pk)
    mime = magic.Magic(mime=True)
    response = HttpResponse(doc.data, content_type=mime.from_buffer(doc.data))
    response['Content-Disposition'] = ('attachment; '
                                       'filename="%s"' % doc.filename)
    return response
