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


Make it run
-----------

*The program needs super user privileges because it runs a web server on port 80 and simulates keyboard events.*

First, do necessary steps to [install Kauko.](https://github.com/kimmobrunfeldt/kauko#installing)

After you have installed it run:

    sudo python main.py

Then browse to your computer's ip address with your device's browser.
   **main.py** prints the address you should browse to but it might not be correct.


Installing
==========

Kauko requires:
 * [gevent](http://www.gevent.org/)
 * [PyMouse](https://github.com/pepijndevos/PyMouse)

They are modules for Python.


OSX
---

Start the terminal application and follow the instructions.

Install [pip](http://pypi.python.org/pypi/pip):

    mkdir build
    cd build
    curl -O http://python-distribute.org/distribute_setup.py
    sudo python distribute_setup
    sudo easy_install pip

After that you have to install [libevent](http://libevent.org/).
Note that gevent starts using [libev](http://software.schmorp.de/pkg/libev.html) starting from 1.0 version.

At the time of writing, pip installs gevent which uses libevent.

Installing libevent:

**To ease your job, a few of the following commands use a wildcard.
You MUST make sure that before you execute these commands,
you don't have any earlier versions of libevent in your Downloads directory!**

Download the latest stable libevent **.tar.gz** file from http://libevent.org to your Downloads directory and run the following commands:

    mv ~/Downloads/libevent-*-stable.tar.gz .
    tar xvvf libevent-*-stable.tar.gz
    cd libevent-*-stable
    ./configure && make
    sudo make install

At this point you have to choose if you want the installation inside
a virtualenv or not. If you want it, move to [Virtualenv](https://github.com/kimmobrunfeldt/kauko#virtualenv).

If you don't care about virtualenv:

    sudo pip install gevent
    sudo pip install PyMouse

    curl -L -O https://github.com/kimmobrunfeldt/kauko/archive/master.zip
    mv kauko-master kauko
    cd kauko

Linux(Ubuntu and other Debian based)
------------------------------------

Run the following commands in terminal:

    # gevent needs python-dev and libevent
    sudo apt-get install git python-pip python-dev libevent-dev

At this point you have to choose if you want the installation inside
a virtualenv or not. If you want it, move to [Virtualenv](https://github.com/kimmobrunfeldt/kauko#virtualenv).

If you don't care about virtualenv:

    sudo pip install gevent
    sudo pip install PyMouse

    git clone https://github.com/kimmobrunfeldt/kauko.git
    cd kauko

    # Install python-xlib
    wget http://sourceforge.net/projects/python-xlib/files/python-xlib/0.15rc1/python-xlib-0.15rc1.tar.gz
    sudo pip install python-xlib-0.15rc1.tar.gz


Virtualenv
----------

I recommend that you install [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html), configure it and use it:

    mkvirtualenv --no-site-packages kauko
    pip install gevent
    pip install PyMouse
    git clone https://github.com/kimmobrunfeldt/kauko.git
    cd kauko


If you are running Linux, also install python-xlib:

    wget http://sourceforge.net/projects/python-xlib/files/python-xlib/0.15rc1/python-xlib-0.15rc1.tar.gz
    pip install python-xlib-0.15rc1.tar.gz


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

In theory any device which has a web browser can be used as a remote control.

OSX and Linux are supported from computer operating systems.
