"""
python-xlib controller.

Uses 'xtest'-extension of X.
"""

import logging
import os
import subprocess

import pymouse
import Xlib
import Xlib.display

import kauko.operatingsystem as operatingsystem
from keyboard import Keyboard


logger = logging.getLogger(__name__)
script_dir = os.path.dirname(os.path.realpath(__file__))


class Mouse(pymouse.PyMouse):
    """Adds double click functionality."""

    def double_click(self, x, y, button=1):
        self.click(x, y, button)
        self.click(x, y, button)


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
            subprocess.call(['xset', 'dpms', 'force', 'off'])
        else:
            subprocess.call(['xset', 'dpms', 'force', 'on'])
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
                key = chr(int(key))
            except TypeError:
                logger.warning("Cant send ascii key: %s, not numeric" % (key))
                return

        logger.debug("send_key %s, type: %s" % (key, key_type))

        if key_type == "str":
            self._keyboard.send_string(key)
        elif key_type == "keycode":
            self._keyboard.send_keycode(key)
        elif key_type == "keysym":
            self._keyboard.send_keysym(key)
        else:
            logger.error("Unknown type of key %s" % key_type)
