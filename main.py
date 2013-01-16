#!/usr/bin/python

"""
Kauko server. Must be run as super user.

Usage:
  sudo ./main.py -v -d

Options:
  -h --help                 Prints this help.
  -v --verbose              Used commands are printed to console.
  -d --debug                Debug information is printed to console.
"""

# WARNING: Do NOT use this as a public web server in any way, this is not safe.
#          The static file server has not been built against any threats.

import logging
import socket
import sys

from gevent import pywsgi

import wsgiserver


def setup_logging(root_logger, level=logging.DEBUG):

    if root_logger.handlers:
        for handler in root_logger.handlers:
            root_logger.removeHandler(handler)

    if level == logging.DEBUG:
        format = '%(asctime)-15s %(name)-15s %(levelname)-8s %(message)s'
    else:
        format = '%(message)s'

    formatter = logging.Formatter(format)
    root_logger.setLevel(level)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    root_logger.addHandler(console_handler)


class NullLog(object):
    """gevent writes directly to stdout, give instance of this class to gevent
    and it will shut up. Errors are still written to stderr though.
    """
    def write(self, *args, **kwargs):
        pass


def main():
    if len(sys.argv) > 1 and sys.argv[1].lower() in ['-h', '--help']:
        print(__doc__.strip())
        sys.exit(0)

    verbose_flag = '-v' in sys.argv[1:] or '--verbose' in sys.argv[1:]
    debug_flag = '-d' in sys.argv[1:] or '--debug' in sys.argv[1:]

    logging_level = logging.WARNING
    if verbose_flag:
        logging_level = logging.INFO

    # If debug is specified, it overrides the verbose flag.
    if debug_flag:
        logging_level = logging.DEBUG

    setup_logging(logging.getLogger(''), level=logging_level)

    print('\nKauko is now started, quit the program by pressing Ctrl - C')
    print('\nOpen the following address in your browser:')
    print('http://%s' % socket.gethostbyname(socket.gethostname()))

    # Serve static files and routes with wsgi app
    if logging_level > logging.DEBUG:
        log = NullLog()
    else:
        log = 'default'  # Uses gevent's default logging -> stdout

    http_server = pywsgi.WSGIServer(('0.0.0.0', 8080), wsgiserver.main_app,
                                    log=log)
    http_server.serve_forever()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Quit.\n')
