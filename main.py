#!/usr/bin/env python

"""
Kauko server. Must be run as super user.

Usage:
  sudo python main.py -v -d
  sudo python main.py -p 8080


Options:
  -h --help                 Prints this help.
  -v --verbose              Used commands are printed to console.
  -d --debug                Debug information is printed to console.
  -p --port=<port>          Web server's listening port.
"""

# WARNING: Do NOT use this as a public web server in any way, this is not safe.
#          The static file server has not been built against any threats.

import logging
import os
import socket
import sys

from gevent import pywsgi

import wsgiserver

script_dir = os.path.dirname(os.path.realpath(__file__))


def get_resource(resource_path):
    """Returns resource's full path from relative path."""
    frozen = getattr(sys, 'frozen', '')

    if not frozen:
        resource_dir = script_dir

    elif frozen in ('dll', 'console_exe', 'windows_exe'):
        # py2exe:
        resource_dir = os.path.dirname(sys.executable)

    elif frozen in ('macosx_app',):
        # py2app:
        # Notes on how to find stuff on MAC, by an expert (Bob Ippolito):
        # http://mail.python.org/pipermail/pythonmac-sig/2004-November/012121.html
        resource_dir = os.environ['RESOURCEPATH']

    return os.path.join(resource_dir, resource_path)


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
    argv = sys.argv[1:]
    if '-h' in argv or '--help' in argv:
        print(__doc__.strip())
        sys.exit(0)

    port = 80
    # Parse port from arguments
    success = True
    for param in ['-p', '--port']:
        if param in argv:
            # Find the index of -p or --port from argv list
            try:
                i = argv.index(param)
            except ValueError:
                success = False
                break

            # Try to convert the following argument to port number.
            try:
                port = int(argv[i + 1])
                if not 1 <= port <= 65535:
                    raise ValueError  # Invalid port number
            except (ValueError, IndexError):
                success = False
                break

    if not success:
        print('Error: Invalid port number.\nUse number between 1-65535.')
        sys.exit(1)

    verbose_flag = '-v' in argv or '--verbose' in argv
    debug_flag = '-d' in argv or '--debug' in argv

    logging_level = logging.WARNING
    if verbose_flag:
        logging_level = logging.INFO

    # If debug is specified, it overrides the verbose flag.
    if debug_flag:
        logging_level = logging.DEBUG

    setup_logging(logging.getLogger(''), level=logging_level)

    print('\nKauko is now started, quit the program by pressing Ctrl - C')
    print('\nOpen the following address in your browser:')

    address = 'http://%s' % socket.gethostbyname(socket.gethostname())
    if port != 80:
        address += ':%s' % port
    print(address)

    # Serve static files and routes with wsgi app
    if logging_level > logging.DEBUG:
        log = NullLog()
    else:
        log = 'default'  # Uses gevent's default logging -> stdout

    http_server = pywsgi.WSGIServer(('0.0.0.0', port), wsgiserver.main_app,
                                    log=log)
    http_server.serve_forever()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Quit.\n')
