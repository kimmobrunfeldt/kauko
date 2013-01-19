"""
python-xlib controller.

Uses 'xtest'-extension of X.
"""

import logging
import os

import pymouse
import Xlib
import Xlib.X
import Xlib.XK
import Xlib.display
import Xlib.protocol.event

import operatingsystem

logger = logging.getLogger(__name__)
script_dir = os.path.dirname(os.path.realpath(__file__))


class Mouse(pymouse.PyMouse):
    """Adds double click functionality."""

    def double_click(self, x, y, button=1):
        self.click(x, y, button)
        self.click(x, y, button)


# Keyboard class needs these
special_X_keysyms = {
    ' ': "space",
    '\t': "Tab",
    '\n': "Return",  # for some reason this needs to be cr, not lf
    '\r': "Return",
    '\e': "Escape",
    '!': "exclam",
    '#': "numbersign",
    '%': "percent",
    '$': "dollar",
    '&': "ampersand",
    '"': "quotedbl",
    '\'': "apostrophe",
    '(': "parenleft",
    ')': "parenright",
    '*': "asterisk",
    '=': "equal",
    '+': "plus",
    ',': "comma",
    '-': "minus",
    '.': "period",
    '/': "slash",
    ':': "colon",
    ';': "semicolon",
    '<': "less",
    '>': "greater",
    '?': "question",
    '@': "at",
    '[': "bracketleft",
    ']': "bracketright",
    '\\': "backslash",
    '^': "asciicircum",
    '_': "underscore",
    '`': "grave",
    '{': "braceleft",
    '|': "bar",
    '}': "braceright",
    '~': "asciitilde"
}


class Keyboard(object):
    """Simulates key events with Xlib library.

    a Python version of crikey,
    http://shallowsky.com/software/crikey
    Simulate keypresses under X11.
    """

    def __init__(self, display):
        super(Keyboard, self).__init__()

        self._display = display

    def send_string(self, string):
        for char in string:
            keycode, shift_mask = self._char_to_keycode(char)
            if shift_mask != 0:
                Xlib.ext.xtest.fake_input(self._display, Xlib.X.KeyPress, 50)

            Xlib.ext.xtest.fake_input(self._display, Xlib.X.KeyPress, keycode)
            Xlib.ext.xtest.fake_input(self._display, Xlib.X.KeyRelease, keycode)

            if shift_mask != 0:
                Xlib.ext.xtest.fake_input(self._display, Xlib.X.KeyRelease, 50)

        self._display.sync()

    def send_keycode(self, key):
        Xlib.ext.xtest.fake_input(self._display, Xlib.X.KeyPress, key)
        Xlib.ext.xtest.fake_input(self._display, Xlib.X.KeyRelease, key)
        self._display.sync()

    def send_keysym(self, keysym):
        key = self._display.keysym_to_keycode(keysym)
        Xlib.ext.xtest.fake_input(self._display, Xlib.X.KeyPress, key)
        Xlib.ext.xtest.fake_input(self._display, Xlib.X.KeyRelease, key)
        self._display.sync()

    def _get_keysym(self, char):
        keysym = Xlib.XK.string_to_keysym(char)
        if keysym == 0:
            # Unfortunately, although this works to get the correct keysym
            # i.e. keysym for '#' is returned as "numbersign"
            # the subsequent display.keysym_to_keycode("numbersign") is 0.
            keysym = Xlib.XK.string_to_keysym(special_X_keysyms[char])
        return keysym

    def _is_shifted(self, char):
        return char.isupper() or char in "~!@#$%^&*()_+{}|:\"<>?"

    def _char_to_keycode(self, char):
        keysym = self._get_keysym(char)
        keycode = self._display.keysym_to_keycode(keysym)
        if keycode == 0:
            logger.error('Cannot map %s.' % char)

        if self._is_shifted(char):
            shift_mask = Xlib.X.ShiftMask
        else:
            shift_mask = 0

        return keycode, shift_mask


class Linux(operatingsystem.BaseOS):
    """Works in operating systems which support Xlib."""

    # from keysymdef. h
    # define XF86XK_AudioLowerVolume 0x1008FF11   /* Volume control down    */
    # define XF86XK_AudioRaiseVolume 0x1008FF13   /* Volume control up      */
    # define XF86XK_AudioNext    0x1008FF17   /* Next track                 */
    # define XF86XK_AudioPrev    0x1008FF16   /* Previous track             */
    # define XF86XK_AudioMute    0x1008FF12   /* Mute sound from the system */
    # define XF86XK_AudioPlay    0x1008FF14   /* Start playing of audio >   */

    KEY_VOLUME_UP = 0x1008FF13
    KEY_VOLUME_DOWN = 0x1008FF11
    KEY_NEXT = 0x1008FF17
    KEY_PREVIOUS = 0x1008FF16
    KEY_MUTE = 0x1008FF12
    KEY_PLAY = 0x1008FF14

    def __init__(self):
        super(Linux, self).__init__()
        self._display = Xlib.display.Display()
        self._mouse = Mouse()
        self._keyboard = Keyboard(self._display)
        self._display_is_asleep = False

    # Public commands

    def toggle_sleep_display(self):
        if not self._display_is_asleep:
            self._display.force_screen_saver(Xlib.X.ScreenSaverActive)
        else:
            self._display.force_screen_saver(Xlib.X.ScreenSaverReset)
        self._display_is_asleep = not self._display_is_asleep

    def volume_up(self):
        self.send_key(key=self.KEY_VOLUME_UP, key_type="keysym")

    def volume_down(self):
        self.send_key(key=self.KEY_VOLUME_DOWN, key_type="keysym")

    def toggle_mute(self):
        self.send_key(key=self.KEY_MUTE, key_type="keysym")

    def previous_track(self):
        self.send_key(key=self.KEY_PREVIOUS, key_type="keysym")

    def next_track(self):
        self.send_key(key=self.KEY_NEXT, key_type="keysym")

    def play_pause(self):
        self.send_key(key=self.KEY_PLAY, key_type="keysym")

    def send_key(self, key, is_ascii=False, key_type="str"):
        if is_ascii:
            try:
                key = int(key)
                key_type = "keycode"
            except TypeError:
                logger.warning("Cant send ascii key: %s, not numeric" % (key))
                return

        logger.debug("send_key %s, type: %s" % (key, key_type))

        if key_type == "str":
            self._keyboard.send_string(key, self._display)
        elif key_type == "keycode":
            self._keyboard.send_keycode(key, self._display)
        elif key_type == "keysym":
            self._keyboard.send_keysym(key, self._display)
        else:
            logger.error("Unknown type of key %s" % key_type)
