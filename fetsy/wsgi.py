import os

from datetime import datetime

from werkzeug.http import http_date
from werkzeug.wsgi import wrap_file


def application(environ, start_response):
    """
    Small WSGI application as helper for development.

    Always send the index.html without any caching. This is only used for
    Crossbar's built-in web service (WSGI Host Service) to serve the
    webclient.
    """
    index_path = os.path.join(os.path.dirname(__file__), 'index.html')
    file = open(index_path, 'rb')
    mtime = datetime.utcfromtimestamp(os.path.getmtime(index_path))
    file_size = int(os.path.getsize(index_path))
    headers = [
        ('Date', http_date()),
        ('Cache-Control', 'public'),
        ('Content-Type', 'text/html'),
        ('Content-Length', str(file_size)),
        ('Last-Modified', http_date(mtime)),
    ]
    start_response('200 OK', headers)
    return wrap_file(environ, file)
