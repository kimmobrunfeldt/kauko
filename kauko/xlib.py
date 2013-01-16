"""
python-xlib controller

uses 'xtest'-extension of X
"""

import logging
import os
import subprocess

try:
    import Xlib
    import Xlib.X
    import xlib_pykey
except Exception as e:
    print "Could not import Xlib, %s"%e
    exit(0)

logger = logging.getLogger(__name__)
script_dir = os.path.dirname(os.path.realpath(__file__))

class xlib(object):
    """xlib controller"""

    #from keysymdef.h
    #define XF86XK_AudioLowerVolume 0x1008FF11   /* Volume control down        */
    #define XF86XK_AudioRaiseVolume 0x1008FF13   /* Volume control up          */
    #define XF86XK_AudioNext    0x1008FF17   /* Next track                 */
    #define XF86XK_AudioPrev    0x1008FF16   /* Previous track             */
    #define XF86XK_AudioMute    0x1008FF12   /* Mute sound from the system */
    #define XF86XK_AudioPlay    0x1008FF14   /* Start playing of audio >   */

    VolUp = 0x1008FF13 
    VolDown = 0x1008FF11
    Next = 0x1008FF17
    Prev = 0x1008FF16
    Mute = 0x1008FF12 
    Play = 0x1008FF14 

    def __init__(self):
        super(xlib, self).__init__()
        self.Xdisplay = Xlib.display.Display()
        self.Xscreen = self.Xdisplay.screen()
        logging.debug('Screen size: %s, %s' % (self.Xscreen["width_in_pixels"],self.Xscreen["height_in_pixels"]))

        self.display_is_asleep = False #meh..


    #Mouse events:
    def _mouse_press(self, x, y, button=1, release=False):
        if button == 1:
            mouse_type = Xlib.X.Button1
        elif button == 2:
            mouse_type = Xlib.X.Button2
        elif button == 3:
            mouse_type = Xlib.X.Button3
        else:
            logging.warning("Unknown button %s"%button)
            return
        if not release:
            Xlib.ext.xtest.fake_input( self.Xdisplay, Xlib.X.ButtonPress, mouse_type )
        else:
            Xlib.ext.xtest.fake_input( self.Xdisplay, Xlib.X.ButtonRelease, mouse_type )


    def _mouse_release(self, x, y, button=1):
        self._mouse_press( x,y,button,release=True)

    def _mouse_move(self, x, y):
        self.Xscreen.root.warp_pointer(x,y)

    def _mouse_position(self):
        p = self.Xscreen.root.query_pointer()._data
        return p["root_x"],p["root_y"]

    def _mouse_click(self,x,y, button=1):
        self._mouse_press(x,y,button)
        self._mouse_release(x,y,button)

    def _mouse_double_click(self, x, y, button=1):
        """button parameter is not currently used."""
        self._mouse_click(x,y,button)
        self._mouse_click(x,y,button)


    #Other helpful methods
    def _screen_size(self):
        return self.Xscreen["widht_in_pixels"],self.Xscreen["height_in_pixels"]


    # Public commands

    def toggle_sleep_display(self):

        if not self.display_is_asleep:
            self.XDisplay.force_screen_saver( Xlib.X.ScreenSaverActive )
        else:
            self.XDisplay.force_screen_saver( Xlib.X.ScreenSaverReset )
        self.display_is_asleep = not self.display_is_asleep

    def volume_up(self):
        self.send_key( key=self.VolUp, key_type="keysym" )

    def volume_down(self):
        self.send_key( key=self.VolDown, key_type="keysym" )

    def toggle_mute(self):
        self.send_key( key=self.Mute, key_type="keysym" )

    def previous_track(self):
        self.send_key( key=self.Prev, key_type="keysym" )

    def next_track(self):
        self.send_key( key=self.Next, key_type="keysym" )

    def play_pause(self):
        self.send_key( key=self.Play, key_type="keysym" )

    def send_key(self, key, is_ascii=False, key_type="str"):
        if is_ascii:
            try:
                key = int(key)
                key_type = "keycode"
            except TypeError:
                logger.warning("Cant send ascii key: %s, not numeric"%(key))
        logger.debug("send_key %s, type: %s"%(key,key_type))

        if key_type=="str":
            xlib_pykey.send_string(key,self.Xdisplay)
        elif key_type=="keycode":
            xlib_pykey.send_keycode(key, self.Xdisplay )
        elif key_type=="keysym":
            xlib_pykey.send_keysym(key, self.Xdisplay )
        else:
            logger.warning("Unknown type of key %s"%key_type)



    def mouse_move(self, x, y, relative=True):
        """Moves mouse cursor to x, y in screen."""

        if relative:
            current_x, current_y = self._mouse_position()
            x = current_x + x
            y = current_y + y

        self._mouse_move(x, y)

    def mouse_click(self, button=1, double=False):
        """Emulates mouse button click. Default is left click.

        Kwargs:
            button: What button of the mouse to emulate.
                    Button is defined as 1 = left, 2 = right, 3 = middle.
        """
        x, y = self._mouse_position()
        if double:
            self._mouse_double_click(x, y, button=button)
        else:
            self._mouse_click(x, y, button=button)
