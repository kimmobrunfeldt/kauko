"""ExampleOS class contains the methods that every OS specific class should
implement.
"""


class ExampleOS(object):
    """Each OS class must provide the same public methods as this class."""
    def __init__(self):
        super(ExampleOS, self).__init__()

    def run(self, name, *args, **kwargs):
        """Runs a predefined script defined in scripts.py."""
        pass

    def send_key(self, key, is_ascii=False):
        """Simulates keypress.

        key: Single unicode character or ASCII number if is_ascii is True.
        is_ascii: Is the key an ASCII character number?
        """
        pass

    def mouse_move(self, x, y, relative=True):
        """Moves mouse cursor to x, y in screen.
        If relative, moves cursor relative to current position.
        """
        pass

    def mouse_click(self, button=1, double=False):
        """Emulates mouse button click. Default is left click.

        Kwargs:
            button: What button of the mouse to emulate.
                    Button is defined as 1 = left, 2 = right, 3 = middle.
        """
        pass
