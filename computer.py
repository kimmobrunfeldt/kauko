"""
Classes to control OS.
"""

import os
import subprocess
import sys
import Quartz

import applescripts


class ExampleOS(object):
    """Each OS class must provide the same public methods as this class."""
    def __init__(self):
        super(OSX, self).__init__()

    def mouse_move(self, x, y, absolute=False):
        """Moves mouse cursor to x, y in screen.
        If absolute is False, mouse is moved relative to current position.
        """
        pass

    def mouse_click(self, button=0):
        """Emulates mouse button click. Default is left click.

        Kwargs:
            button: What button of the mouse to emulate. Valid numbers 0 - n.
                    Where n - 1 is the number of buttons in the mouse.
        """
        pass

    def send_key(self, key):
        """Emulates key press. Key """
        pass

    def volume_up(self):
        """Increases system volume."""
        pass

    def volume_down(self):
        """Decreases system volume."""
        pass

    def next_track(self):
        """Switches to next track."""
        pass

    def previous_track(self):
        """Switches to previous track."""
        pass

    def play(self):
        """Plays media."""
        pass

    def pause(self):
        """Pauses media."""
        pass

    def shutdown(self):
        """Shutdowns computer."""
        pass


class OSX(object):
    """OSX specific."""

    # NSEvent.h
    NSSystemDefined = 14

    # hidsystem/ev_keymap.h
    NX_KEYTYPE_SOUND_UP = 0
    NX_KEYTYPE_SOUND_DOWN = 1
    NX_KEYTYPE_PLAY = 16
    NX_KEYTYPE_NEXT = 17
    NX_KEYTYPE_PREVIOUS = 18
    NX_KEYTYPE_FAST = 19
    NX_KEYTYPE_REWIND = 20

    def __init__(self):
        super(OSX, self).__init__()

    def _run(self, code):
        subprocess.call(['osascript', '-e', code])

    def _send_media_key(self, key):
        """Sends key using Quartz. Valid values are self.NX_KEYTYPE_...
        defined in this class.
        """
        def doKey(down):
            ev = Quartz.NSEvent.otherEventWithType_location_modifierFlags_timestamp_windowNumber_context_subtype_data1_data2_(
                self.NSSystemDefined,  # type
                (0, 0),  # location
                0xa00 if down else 0xb00,  # flags
                0,  # timestamp
                0,  # window
                0,  # ctx
                8,  # subtype
                (key << 16) | ((0xa if down else 0xb) << 8),  # data1
                -1  # data2
                )
            cev = ev.CGEvent()
            Quartz.CGEventPost(0, cev)

        doKey(True)
        doKey(False)

    # Public commands

    def mouse_move(self, x, y):
        pass

    def mouse_click(self, button=0):
        pass

    def send_key(self, key):
        pass

    def volume_up(self):
        self._send_media_key(self.NX_KEYTYPE_SOUND_UP)

    def volume_down(self):
        self._send_media_key(self.NX_KEYTYPE_SOUND_DOWN)

    def previous_track(self):
        self._send_media_key(self.NX_KEYTYPE_REWIND)

    def next_track(self):
        self._send_media_key(self.NX_KEYTYPE_FAST)


# Mac
if sys.platform.startswith('darwin'):
    _computer = OSX()

# Windows
elif os.name == 'nt':
    raise NotImplemented('Windows in not supported yet.')

# *nix(Linux etc.)
elif os.name == 'posix':
    raise NotImplemented('Linux in not supported yet.')


def command(command, args, kwargs):
    """Returns success of command."""
    print command, args, kwargs

    try:
        method = getattr(_computer, command)
    except AttributeError:
        return False

    return method(*args, **kwargs)
