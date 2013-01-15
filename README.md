# Kauko

Kauko is a remote control for computer. Turn almost any device into a remote control!

![SCREENSHOT](https://github.com/kimmobrunfeldt/kauko/raw/master/static/img/screenshot.png)


What are the benefits
---------------------

You can use almost any mobile device or even another computer to control your primary computer.

No more problems like this:

![PROBLEM](https://github.com/kimmobrunfeldt/kauko/raw/master/static/img/problem.png)

How it works
------------

Computer runs a web server which serves the remote control web page for devices.

**WARNING:** Using this program might be a security risk! Anyone who can access the web page, can control your computer.


Installing
==========

Kauko requires gevent( http://www.gevent.org/ ) module for Python.

Virtualenv
----------

Installing to virtualenv is simple:

    mkvirtualenv --no-site-packages kauko
    pip install gevent
    git clone https://github.com/kimmobrunfeldt/kauko.git


Make it run
-----------

The program needs super user privileges because it runs a web server on port 80 and simulates keyboard events.

After you have installed it run:

    sudo python main.py

Then browse to your computer's ip address with your device's browser.
   **main.py** prints the address you should browse to but it might not be correct.


Problems
========

This has been tested and works well with iPad. However there are many problems with other devices and their browsers.

    socket.error: [Errno 13] Permission denied: ('0.0.0.0', 80)

**main.py** has to be run as super user.

OSX
---

    ImportError: No module named Quartz

This shouldn't happen because Quartz's location is added to sys.path in **osx.py**.

Anyway, Quartz is the library which is used to simulate keyboard and mouse events. Quartz is importable in OSX's default python located in **/usr/bin/python**.
Module should be located in /System/Library/Frameworks/Python.framework/Versions/X.X/Extras/lib/python/PyObjC, where X.X corresponds to Python's version(e.g. 2.7).

Supported operating systems
----------------------------

Currently only OSX is supported, but any device that has a web browser can be used as a remote control.
