import os.path

from django.http import HttpResponse

from cmis_storage.storage import CMISStorage


def get_file(request, path):
    """
    Returns a file stored in the CMIS-compatible content management system

    :param path: The full path of the file within the CMS
    """
    _, filename = os.path.split(path)

    storage = CMISStorage()
    stream = storage.open_stream(path)

    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    response.write(stream.read())

    return response
