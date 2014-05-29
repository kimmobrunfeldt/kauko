
import Xlib
import Xlib.X
import Xlib.XK
import Xlib.display
import Xlib.protocol.event
import Xlib.keysymdef.xkb


special_X_keysyms = {
    u'\x08': "BackSpace",
    u'\n': "Return",  # for some reason this needs to be cr, not lf
    u'\r': "Return",
}


class Keyboard(object):
    """Simulates key events with Xlib library.

    a Python version of crikey,
    http://shallowsky.com/software/crikey
    Simulate keypresses under X11.

    This is how xte from xautomation does emulating strings:
    http://sourcecodebrowser.com/xautomation/1.03/xte_8c.html#a663f8d2c2df1e8f889ee4d257e2b57f7

    keysym term means a constant that Xlib uses to identify each key. They
    do not depend on the keyboard layout.

    keycode means the raw keycode which Xlib will send based on keysym.
    keycode depends on the keyboard layout
    """

    # Keysyms for modifier keys
    KEYSYM_ALTGR = Xlib.keysymdef.xkb.XK_ISO_Level3_Shift
    KEYSYM_SHIFT = Xlib.XK.string_to_keysym('Shift_L')

    def __init__(self, display):
        super(Keyboard, self).__init__()

        self._display = display

    def send_string(self, string):
        for char in string:
            self.send_ord(ord(char))

    def send_keycode(self, keycode):
        Xlib.ext.xtest.fake_input(self._display, Xlib.X.KeyPress, keycode)
        Xlib.ext.xtest.fake_input(self._display, Xlib.X.KeyRelease, keycode)
        self._display.sync()

    def send_keysym(self, keysym):
        keycode = self._display.keysym_to_keycode(keysym)
        Xlib.ext.xtest.fake_input(self._display, Xlib.X.KeyPress, keycode)
        Xlib.ext.xtest.fake_input(self._display, Xlib.X.KeyRelease, keycode)
        self._display.sync()

    def send_ord(self, char_ord):
        """Sends character based on it's unicode value.
        For example, char_ord = 228, would send u'\xe4'.
        ord(u'\xe4') == 228
        """
        # List of (keycode, modifier) pairs which produce the given char.
        keycodes = self._keysym_to_keycode(char_ord)

        if keycodes is None:
            try:
                keysym_short = special_X_keysyms[unichr(char_ord)]
            except KeyError:
                logger.error('Could not send keysym %s.' % char_ord)
                return

            keysym = Xlib.XK.string_to_keysym(keysym_short)
            keycodes = self._keysym_to_keycode(keysym)
            if keycodes is None:
                logger.error('Could not send %s %s.' % (keysym_short, keysym))
                return

        keycode, modifier = keycodes[0]

        # I didn't figure out how to use the returned modifier in a common
        # case. I just decided that 1 is shift and others use alt gr.
        # It doesn't work for dead keys etc.
        # I tried to:
        #  mapping = self._display.get_modifier_mapping()
        #  modifier_key = mapping[modifier - 1][0]
        #
        # But for example character @(64) did not produce the right modifier.
        # It should have produced alt gr, but the keycode was not correct.
        # Even though the Xlib.display.keycode_to_keysym(key, index) told that
        # the returned pair would produce character @, it actually did not.

        # If the modifier is 1 use shift, otherwise use alt gr
        modifier_keysym = self.KEYSYM_SHIFT
        if modifier != 1:
            modifier_keysym = self.KEYSYM_ALTGR

        modifier_keycode = self._display.keysym_to_keycode(modifier_keysym)

        if modifier:
            Xlib.ext.xtest.fake_input(self._display, Xlib.X.KeyPress,
                                      modifier_keycode)

        Xlib.ext.xtest.fake_input(self._display, Xlib.X.KeyPress, keycode)
        Xlib.ext.xtest.fake_input(self._display, Xlib.X.KeyRelease, keycode)

        if modifier:
            Xlib.ext.xtest.fake_input(self._display, Xlib.X.KeyRelease,
                                      modifier_keycode)

        self._display.sync()

    def _keysym_to_keycode(self, keysym):
        keycodes = self._display.keysym_to_keycodes(keysym)
        if len(keycodes) > 0:
            return keycodes

        return None
