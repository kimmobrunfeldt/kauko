#!/bin/env python
# vim:fileencoding=utf-8:ft=python
#
"""
	Paste a password from a GPG encrypted password file to open
	applications.
	Copyright (c) 2007, Phillip Berndt

	You should bind this script to a hotkey in your WM.
	The password file must be located in ~/.myshadow. This script will
	ignore all lines in this file except for those matching the following
	pattern:

	r/regex-window-match/ <whitespace> password
	q/search-text/ <whitespace> password

	Remember that r/../ must MATCH against the window title. i.E. "firefox"
	will never match as Firefox windows are at least titled "Mozilla
	Firefox".
	The first match is always taken.
"""
import sys
import re
import os
try:
	import Xlib.display, Xlib.XK
except:
	print >> sys.stderr, (
		"This script needs the python Xlib bindings\n"
		"Download them at http://python-xlib.sourceforge.net"
		)
	sys.exit(1)
try:
	import gtk
except:
	print >> sys.stderr, (
		"This script needs pyGTK\n",
		"Download it at http://www.pygtk.org"
		)
	sys.exit(1)

def errorMessage(msg):
	"""
		Show an error message dialog
	"""
	dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, msg)
	dialog.set_title("passwrd: Failure")
	dialog.run()
	dialog.hide()
	gtk.main_iteration_do()
	dialog.destroy()
	gtk.main_iteration_do()

def ask(title, question, isq = False):
	"""
		Ask for something and return it
	"""
	def hide(x):
		pWindow.hide()
		gtk.main_quit()
	pWindow = gtk.Window()
	pWindow.connect("hide", hide)
	pWindow.set_title("passwrd: " + title)
	pWindow.set_default_size(300, 120)
	pWindow.set_border_width(10)
	pWindow.set_position(gtk.WIN_POS_MOUSE)
	pVbox = gtk.VBox()
	pWindow.add(pVbox)
	pHbox = gtk.HBox()
	pVbox.add(pHbox)
	if isq:
		pImage = gtk.image_new_from_icon_name("gtk-dialog-question", 3)
	else:
		pImage = gtk.image_new_from_icon_name("gtk-dialog-authentication", 3)
	pHbox.add(pImage)
	pLabel = gtk.Label(question)
	pLabel.set_padding(3, 3)
	pHbox.add(pLabel)
	pEntry  = gtk.Entry()
	pEntry.set_activates_default(True)
	if not isq:
		pEntry.set_visibility(False)
	pVbox.add(pEntry)
	pButton = gtk.Button()
	pButton.set_label("Ok")
	pButton.connect("clicked", hide)
	pButton.set_flags(gtk.CAN_DEFAULT)
	pButton.set_image(gtk.image_new_from_icon_name("gtk-ok", -1))
	pWindow.set_default(pButton)
	pHbox2 = gtk.HBox()
	pHbox2.add(gtk.Label())
	pHbox2.add_with_properties(pButton, "expand", False, "fill", False)
	pHbox2.add(gtk.Label())
	pVbox.add(pHbox2)
	pWindow.show_all()
	if not isq:
		root = gtk.gdk.get_default_root_window()
		gtk.gdk.keyboard_grab(root, True, gtk.get_current_event_time())
		gtk.gdk.pointer_grab(root, True, 0, None, None, gtk.get_current_event_time())
		pEntry.grab_focus()
	gtk.main()
	return pEntry.get_text()

def windowName(widget):
	"""
		Get the window-wm-title of the parent window of a widget having
		the focus
	"""
	wmName = widget.get_wm_name()
	while not wmName:
		query = widget.query_tree()
		if query.parent == query.root:
			return "-unknown-"
		widget = query.parent
		wmName = widget.get_wm_name()
	return wmName

def sendString(target, text):
	"""
		Send a string to <target> window
	"""
	Xlib.XK.load_keysym_group("xkb")
	for char in range(len(text)):
		keySym = Xlib.XK.string_to_keysym(text[char])
		if not keySym:
			keySym = ord(text[char])
		keyCode, index = display.keysym_to_keycodes(keySym)[0]
		mstate = 0
		if index & 1:
			# Shift
			mstate = 1
		if index & 2:
			# Alt Grid
			mstate = mstate | 0x80
		for mtype in (Xlib.protocol.event.KeyPress, Xlib.protocol.event.KeyRelease):
			ev = mtype(time=0, child=0, state=mstate, root=target.query_tree().root, window=target, same_screen=1, \
				root_x=0, root_y=0, event_x=0, event_y=1, detail=keyCode)
			target.send_event(ev)
			display.sync()

if __name__ == "__main__":
	# Open display
	try:
		display = Xlib.display.Display()
	except:
		print >> sys.stderr, "Failed to open the display"
		sys.exit(1)

	# Get the active window (widget)
	focusWidget = display.get_input_focus().focus

	# Get wm title
	title = windowName(focusWidget)

	# Load the passfile
	passText = ""
	passphraseFile = os.pipe()
	os.write(passphraseFile[1], ask("Enter passphrase", "Enter your GPG passphrase for \n" + title) + "\n")
	pwData = os.popen("gpg -d --passphrase-fd %d --batch -q --no-tty <~/.myshadow" % passphraseFile[0]).readlines()
	for fd in passphraseFile:
		os.close(fd)
	del passphraseFile
	if len(pwData) == 0:
		errorMessage("Failed to decrypt the shadow file.")
		sys.exit(1)

	# Match wm title against lines
	for line in pwData:
		lineData = re.match("r/([^/]+)/\s+(.+)", line)
		if not lineData:
			continue
		if not re.match(lineData.group(1), title):
			continue
		passText = lineData.group(2).strip()

	if not passText:
		search = ask("Enter search string", "Which password do you want?", True)
		for line in pwData:
			lineData = re.match("q/([^/]+)/\s+(.+)", line)
			if not lineData:
				continue
			if lineData.group(1).lower().find(search.lower()) > -1:
				passText = lineData.group(2).strip()
				break
	if not passText:
		errorMessage("Failed to find a password.")
	else:
		# Send keyboard events
		sendString(focusWidget, passText)
