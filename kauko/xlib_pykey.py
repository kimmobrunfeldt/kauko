#!/usr/bin/env python

# pykey -- a Python version of crikey,
# http://shallowsky.com/software/crikey
# Simulate keypresses under X11.
#
# This software is copyright 2008 by Akkana Peck.
# Please share and re-use this under the terms of the GPLv2
# or, at your option, any later GPL version.

import Xlib.display
import Xlib.X
import Xlib.XK
import Xlib.protocol.event

special_X_keysyms = {
    ' ' : "space",
    '\t' : "Tab",
    '\n' : "Return",  # for some reason this needs to be cr, not lf
    '\r' : "Return",
    '\e' : "Escape",
    '!' : "exclam",
    '#' : "numbersign",
    '%' : "percent",
    '$' : "dollar",
    '&' : "ampersand",
    '"' : "quotedbl",
    '\'' : "apostrophe",
    '(' : "parenleft",
    ')' : "parenright",
    '*' : "asterisk",
    '=' : "equal",
    '+' : "plus",
    ',' : "comma",
    '-' : "minus",
    '.' : "period",
    '/' : "slash",
    ':' : "colon",
    ';' : "semicolon",
    '<' : "less",
    '>' : "greater",
    '?' : "question",
    '@' : "at",
    '[' : "bracketleft",
    ']' : "bracketright",
    '\\' : "backslash",
    '^' : "asciicircum",
    '_' : "underscore",
    '`' : "grave",
    '{' : "braceleft",
    '|' : "bar",
    '}' : "braceright",
    '~' : "asciitilde"
    }


def get_keysym(ch) :
    keysym = Xlib.XK.string_to_keysym(ch)
    if keysym == 0 :
        # Unfortunately, although this works to get the correct keysym
        # i.e. keysym for '#' is returned as "numbersign"
        # the subsequent display.keysym_to_keycode("numbersign") is 0.
        keysym = Xlib.XK.string_to_keysym(special_X_keysyms[ch])
    return keysym

def is_shifted(ch) :
    if ch.isupper() :
        return True
    if "~!@#$%^&*()_+{}|:\"<>?".find(ch) >= 0 :
        return True
    return False

def char_to_keycode(ch, display) :
    keysym = get_keysym(ch)
    keycode = display.keysym_to_keycode(keysym)
    if keycode == 0 :
        print "Sorry, can't map", ch

    if (is_shifted(ch)) :
        shift_mask = Xlib.X.ShiftMask
    else :
        shift_mask = 0

    return keycode, shift_mask


def send_string( str, display ):
    for ch in str :
        keycode, shift_mask = char_to_keycode(ch, display)
        if shift_mask != 0 :
            Xlib.ext.xtest.fake_input(display, Xlib.X.KeyPress, 50)
        Xlib.ext.xtest.fake_input(display, Xlib.X.KeyPress, keycode)
        Xlib.ext.xtest.fake_input(display, Xlib.X.KeyRelease, keycode)
        if shift_mask != 0 :
            Xlib.ext.xtest.fake_input(display, Xlib.X.KeyRelease, 50)
    display.sync()

def send_keycode( key, display ):
    Xlib.ext.xtest.fake_input(display, Xlib.X.KeyPress, key)
    Xlib.ext.xtest.fake_input(display, Xlib.X.KeyRelease, key)
    display.sync()

def send_keysym( keysym, display ):
    key = display.keysym_to_keycode( keysym )
    Xlib.ext.xtest.fake_input(display, Xlib.X.KeyPress, key)
    Xlib.ext.xtest.fake_input(display, Xlib.X.KeyRelease, key)
    display.sync()


