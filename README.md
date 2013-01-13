Kauko
=====

Kauko is remote control for a computer. Turn almost any device into a remote controller!

![LOGO](https://github.com/kimmobrunfeldt/kauko/raw/master/static/img/kauko.png)

Client runs in your device's web browser.
The computer you want to control runs a webserver written in Python.

Requirements
------------

- Python ( http://www.python.org/ )
- gevent ( http://www.gevent.org/ )

Make it run
-----------

Note that the program needs super user privileges because it runs a web server on port 80.

1. Install gevent.

        pip install gevent

2. Open terminal and run main.py

        sudo ./main.py

3. Browse to your computer's ip address with your browser.
   main.py prints your ip address but it might not be correct.
