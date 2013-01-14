Kauko
=====

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

**NOTE:** The program needs super user privileges because it runs a web server on port 80 and simulates keyboard events.

Easy way
--------

**The easy way doesn't work yet, working on it..**

Simplest way to get Kauko running is to download the zipped Kauko.app from:
https://github.com/kimmobrunfeldt/kauko/blob/master/dist/Kauko.zip?raw=true

Unzip the Kauko.zip to for example Downloads folder and run Kauko in terminal:

    cd  # Go to home
    sudo Downloads/Kauko.app/Contents/MacOS/Kauko

**Don't** run the Kauko.app by double clicking it in Finder! It doesn't have any graphical interface yet so it has to be run in terminal.

Hard way
--------

1. Install gevent( http://www.gevent.org/ ) which is a package for Python. If you have pip installed, installing is simple:

        pip install gevent

2. Open terminal and run main.py

        sudo ./main.py

3. Browse to your computer's ip address with your device's browser.
   **main.py** prints the address you should browse to but it might not be correct.

This has been tested and works well with iPad. However there are many problems with other devices and their browsers.

Problems
--------

Installing Kauko to virtualenv causes problems with Quartz if --no-site-packages flag is used:

    ImportError: No module named Quartz

Quartz is the library which is used to simulate keyboard and mouse events. Quartz is importable in OSX's default python located in **/usr/bin/python**.


Supported operating systems
----------------------------

Currently only OSX is supported, but any device that has a web browser can be used as a remote control.
