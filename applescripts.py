"""
Contains apple scripts for certain tasks.
"""

volume_up = """
set currentVolume to output volume of (get volume settings)
if currentVolume < 90 then
   set newVolume to currentVolume + 10
else
   set newVolume to 100
end if
set volume output volume newVolume
"""

kvolume_up = """
tell application "System Events"

    keystroke "F12" using {command down}
end tell
"""

volume_down = """
set currentVolume to output volume of (get volume settings)
if currentVolume > 10 then
   set newVolume to currentVolume - 10
else
   set newVolume to 1
end if
set volume output volume newVolume
"""
