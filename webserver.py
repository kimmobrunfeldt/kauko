#!/usr/bin/python

"""
WARNING: Do NOT use this as a public web server in any way, this is only for
         testing purposes.
"""

import logging
import sys

from gevent import pywsgi

import wsgiserver


def setup_logging(root_logger):
    format = '%(asctime)-15s %(name)-15s %(levelname)-8s %(message)s'
    formatter = logging.Formatter(format)
    root_logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(console_handler)


def main():
    setup_logging(logging.getLogger(''))

    # Serve static files and routes with wsgi app
    http_server = pywsgi.WSGIServer(('0.0.0.0', 80), wsgiserver.main_app)
    http_server.serve_forever()


if __name__ == '__main__':
    main()
