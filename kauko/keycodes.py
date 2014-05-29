"""
Keycode definitions.

Apple:
http://www.opensource.apple.com/source/IOHIDFamily/IOHIDFamily-86.1/IOHIDSystem/IOKit/hidsystem/ev_keymap.h

Linux(X):
What kauko calls raw keycodes actually mean keysyms from X's perspective.
http://cgit.freedesktop.org/xorg/proto/x11proto/plain/keysymdef.h
http://cgit.freedesktop.org/xorg/proto/x11proto/tree/XF86keysym.h

Windows:
http://msdn.microsoft.com/en-us/library/windows/desktop/dd375731(v=vs.85).aspx
"""

# These keycodes are translated to system's keycodes.
# Sending a kauko_key_* should work on each operating system.
kauko_key_volume_up             = 1
kauko_key_volume_down           = 2
kauko_key_volume_mute           = 3
kauko_key_play_pause            = 4
kauko_key_next_track            = 5
kauko_key_previous_track        = 6

# These work ONLY with OSX and Linux.
# Apparently windows does not have the following keys.
kauko_key_fast                  = 7
kauko_key_rewind                = 8
kauko_key_eject                 = 9
kauko_key_power                 = 10


# Translations of general kauko key constants to each platform.
# These are called raw keycodes in Kauko even though at system level they
# may or may not be raw keycodes.
platform_keys = {

    "osx": {
        kauko_key_volume_up: 0,
        kauko_key_volume_down: 1,
        kauko_key_volume_mute: 7,
        kauko_key_play_pause: 16,
        kauko_key_next_track: 17,
        kauko_key_previous_track: 18,
        kauko_key_fast: 19,
        kauko_key_rewind: 20,
        kauko_key_eject: 14,
        kauko_key_power: 6
    },

    "linux": {
        kauko_key_volume_up: 0x1008FF13,
        kauko_key_volume_down: 0x1008FF11,
        kauko_key_volume_mute: 0x1008FF12,
        kauko_key_play_pause: 0x1008FF14,
        kauko_key_next_track: 0x1008FF17,
        kauko_key_previous_track: 0x1008FF16,
        kauko_key_fast: 0x1008FF97,
        kauko_key_rewind: 0x1008FF3E,
        kauko_key_eject: 0x1008FF2C,
        kauko_key_power: 0x1008FF2A
    },

    "windows": {
        kauko_key_volume_up: 0xAF,
        kauko_key_volume_down: 0xAE,
        kauko_key_volume_mute: 0xAD,
        kauko_key_play_pause: 0xB3,
        kauko_key_next_track: 0xB0,
        kauko_key_previous_track: 0xB1
    }

}
