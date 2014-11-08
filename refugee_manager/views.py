import os.path

from django.http import Http404
from django.conf import settings

from sendfile import sendfile

def serve_file(request, filename):
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.abspath(filepath).startswith(settings.MEDIA_ROOT):
        return sendfile(request, filepath)
    else:
        raise Http404