"""
Windows speficic code.
"""

import pymouse
import win32api
import win32gui
import win32con

import operatingsystem


class Mouse(pymouse.PyMouse):
    """Adds double click functionality."""

    def double_click(self, x, y, button=1):
        self.click(x, y, button)
        self.click(x, y, button)


class Windows(operatingsystem.BaseOS):
    """Uses Windows' API to simulate mouse and keyboard events."""

    SC_MONITORPOWER = 0xF170
    MONITOR_POWER_ON = -1
    MONITOR_POWER_OFF = 2

    VK_VOLUME_UP = 0xAF
    VK_VOLUME_DOWN = 0xAE
    VK_VOLUME_MUTE = 0xAD
    VK_MEDIA_NEXT_TRACK = 0xB0
    VK_MEDIA_PREV_TRACK = 0xB1
    VK_MEDIA_PLAY_PAUSE = 0xB3

    def __init__(self):
        super(Windows, self).__init__()
        self._mouse = Mouse()
        self._display_is_asleep = False

    def _send_key(self, vk_code):
        """Sends key based on virtual keycode."""
        hwcode = win32api.MapVirtualKey(vk_code, 0)
        win32api.keybd_event(vk_code, hwcode)

    # Public commands

    def toggle_sleep_display(self):
        if not self._display_is_asleep:
            win32gui.SendMessage(
                win32con.HWND_BROADCAST,
                win32con.WM_SYSCOMMAND,
                self.SC_MONITORPOWER,
                self.MONITOR_POWER_OFF)
        else:
            win32gui.SendMessage(
                win32con.HWND_BROADCAST,
                win32con.WM_SYSCOMMAND,
                self.SC_MONITORPOWER,
                self.MONITOR_POWER_ON)
        self._display_is_asleep = not self._display_is_asleep

    def volume_up(self):
        self._send_key(self.VK_VOLUME_UP)

    def volume_down(self):
        self._send_key(self.VK_VOLUME_DOWN)

    def toggle_mute(self):
        self._send_key(self.VK_VOLUME_MUTE)

    def previous_track(self):
        self._send_key(self.VK_MEDIA_PREV_TRACK)

    def next_track(self):
        self._send_key(self.VK_MEDIA_NEXT_TRACK)

    def play_pause(self):
        self._send_key(self.VK_MEDIA_PLAY_PAUSE)

    def send_key(self, key, is_ascii=False, key_type="str"):
        if is_ascii:
            pass
