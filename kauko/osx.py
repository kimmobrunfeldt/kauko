"""
OSX specific code.
"""

import logging
import subprocess

# If for example virtualenv is used, path to Apple's Quartz must be added
# to Python path.
try:
    import Quartz
except ImportError:
    import sys
    version = '%s.%s' % sys.version_info[:2]
    sys.path.append('/System/Library/Frameworks/Python.framework/Versions/%s/Extras/lib/python/PyObjC' % version)

    import Quartz

from Quartz import CGEventCreateMouseEvent, CGEventSetType
from Quartz import CGEventPost, CGEventSetIntegerValueField
from Quartz.CoreGraphics import kCGEventLeftMouseDown, kCGEventLeftMouseUp
from Quartz.CoreGraphics import CGWarpMouseCursorPosition
from Quartz.CoreGraphics import kCGMouseButtonLeft, kCGMouseEventClickState
from Quartz.CoreGraphics import kCGHIDEventTap

import pymouse

import path

logger = logging.getLogger(__name__)


# https://developer.apple.com/library/mac/#documentation/Carbon/Reference/QuartzEventServicesRef/Reference/reference.html#//apple_ref/c/func/CGEventCreateMouseEvent
class PyMouse(pymouse.PyMouse):
    """Adds double click and uses different function to move mouse."""

    def move(self, x, y):
        CGWarpMouseCursorPosition((float(x), float(y)))

    def double_click(self, x, y, button=1):
        """button parameter is not currently used."""
        event = CGEventCreateMouseEvent(
                        None,
                        kCGEventLeftMouseDown,
                        (x, y),
                        kCGMouseButtonLeft)

        CGEventSetIntegerValueField(event, kCGMouseEventClickState, 2)
        CGEventPost(kCGHIDEventTap, event)

        CGEventSetType(event, kCGEventLeftMouseUp)
        CGEventPost(kCGHIDEventTap, event)
        CGEventSetType(event, kCGEventLeftMouseDown)
        CGEventPost(kCGHIDEventTap, event)
        CGEventSetType(event, kCGEventLeftMouseUp)
        CGEventPost(kCGHIDEventTap, event)


class OSX(object):
    """OSX specific."""

    # NSEvent.h
    NSSystemDefined = 14

    # hidsystem/ev_keymap.h
    NX_KEYTYPE_SOUND_UP = 0
    NX_KEYTYPE_SOUND_DOWN = 1
    NX_KEYTYPE_MUTE = 7
    NX_KEYTYPE_PLAY = 16
    NX_KEYTYPE_NEXT = 17
    NX_KEYTYPE_PREVIOUS = 18
    NX_KEYTYPE_FAST = 19
    NX_KEYTYPE_REWIND = 20

    def __init__(self):
        super(OSX, self).__init__()
        self.mouse = PyMouse()

    def _run(self, code):
        logging.debug('Running "%s"' % code)
        subprocess.call(['osascript', '-e', code])

    def _send_media_key(self, key):
        """Sends key using Quartz. Valid values are self.NX_KEYTYPE_...
        defined in this class.

        Main part taken from http://stackoverflow.com/questions/11045814/emulate-media-key-press-on-mac
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

    def toggle_sleep_display(self):
        display_is_asleep = Quartz.CGDisplayIsAsleep(0)

        program_path = path.get_resource('vendor/SleepDisplay')
        if not display_is_asleep:
            subprocess.call([program_path])

        else:
            subprocess.call([program_path, '--wake'])

    def volume_up(self):
        self._send_media_key(self.NX_KEYTYPE_SOUND_UP)

    def volume_down(self):
        self._send_media_key(self.NX_KEYTYPE_SOUND_DOWN)

    def toggle_mute(self):
        self._send_media_key(self.NX_KEYTYPE_MUTE)

    def previous_track(self):
        self._send_media_key(self.NX_KEYTYPE_REWIND)

    def next_track(self):
        self._send_media_key(self.NX_KEYTYPE_FAST)

    def play_pause(self):
        self._send_media_key(self.NX_KEYTYPE_PLAY)

    def send_key(self, key, is_key_code=False, is_ascii=False):
        if key == '\\':
            key = '92'
            is_ascii = True

        beginning = 'tell application "System Events" to'
        if not is_key_code:
            if not is_ascii:
                self._run('%s keystroke "%s"' % (beginning, key))
            else:
                self._run('%s keystroke (ASCII character %s)' % (beginning,
                                                                 key))
        else:
            self._run('%s key code %s' % (beginning, key))

    def mouse_move(self, x, y, relative=True):
        """Moves mouse cursor to x, y in screen."""

        if relative:
            current_x, current_y = self.mouse.position()
            x = current_x + x
            y = current_y + y

        self.mouse.move(x, y)

    def mouse_click(self, button=1, double=False):
        """Emulates mouse button click. Default is left click.

        Kwargs:
            button: What button of the mouse to emulate.
                    Button is defined as 1 = left, 2 = right, 3 = middle.
        """
        x, y = self.mouse.position()
        if double:
            self.mouse.double_click(x, y, button=button)
        else:
            self.mouse.click(x, y, button=button)
