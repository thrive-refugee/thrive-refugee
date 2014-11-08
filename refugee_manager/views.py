import os.path

from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.conf import settings

from sendfile import sendfile

from refugee_manager.models import Case

def serve_file(request, filename):
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    if not os.path.abspath(filepath).startswith(settings.MEDIA_ROOT):
        # trying to get outside of MEDIA_ROOT
        raise Http404

    upload_type, case_id, file = filename.split('/', 2)  # e.g. case/12/myupload.pdf
    if upload_type == 'case':
        case = Case.objects.get(id=int(case_id))
        if request.user.is_superuser or request.user in [v.user for v in case.volunteers.all()]:
            return sendfile(request, filepath)
        else:
            raise PermissionDenied()
    else:
        raise Http404


