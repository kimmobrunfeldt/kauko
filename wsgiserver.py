#!/usr/bin/python

"""
WSGI middleware app to serve static files and the controlling system.
"""

import json
import logging
import mimetypes
import os
import urlparse

import computer

browserLogger = logging.getLogger('browser')


def filepath(request_path):
    """Returns full filepath from request path.

    WARNING: This is not safe, one could use .. tricks to get into root path!!
    """

    if not request_path.startswith('/'):
        request_path += '/'

    this_path = os.path.dirname(__file__)
    return os.path.abspath(this_path + request_path)


def readfile(path):
    if not os.path.isfile(path):
        return None
    return open(path, 'rb').read()


def file_response(request_path, start_response):
    path = filepath(request_path)

    content = readfile(path)
    if content is not None:
        content_type = mimetypes.guess_type(path)[0]
        start_response('200 OK', [('Content-Type', content_type)])
        return [content]

    return notfound(start_response)


def notfound(start_response):
    start_response('404 Not Found', [('Content-Type', 'text/plain')])
    return ['Not found']


def get_post_data(env):
    """Returns POST data as a dict."""
    body = ''
    try:
        length = int(env.get('CONTENT_LENGTH', '0'))
    except ValueError:
        length = 0
    if length != 0:
        body = env['wsgi.input'].read(length)
    return body


def debug(env, start_response):
    """Mobile devices can send debug information with this route"""
    data = get_post_data(env)
    data = urlparse.parse_qs(data)
    browserLogger.debug(data)

    start_response('200 OK', [])
    return ['']


def main_app(env, start_response):
    """Provides following features:
    - Serves static files
    - /debug route for mobile debugging
    """
    request_path = env['PATH_INFO']

    if request_path == '/debug':
        return debug(env, start_response)

    elif request_path == '/command':
        data = json.loads(get_post_data(env))
        command, args, kwargs = data[0], data[1], data[2]
        computer.command(command, args, kwargs)

        start_response('200 OK', [])
        return ['']

    # Serve a file if it's found.
    else:
        if request_path == '/':
            request_path = '/static/index.html'

        return file_response(request_path, start_response)
