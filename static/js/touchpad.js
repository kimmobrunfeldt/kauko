// Depends from jQuery, because of $.extend. That's a bit senseless.

var TouchPad = (function(options) {

    var defaultOptions = {
        // The maximum difference in swipe x and y that will generate a tap.
        maxTapDistance: 1,
        callbacks: {
            'onetap': function() { },
            'twotap': function() { },
            'move': function() { }
        }
    };

    var my = {},
        options = $.extend(true, {}, defaultOptions, options),
        startX,
        startY,
        lastX,
        lastY,
        lastOneTapTime = new Date().getTime(),
        lastTwoTapTime = new Date().getTime(),
        downPointers = [];

    function init() {
        bindEvents();
    }

    //
    // Public methods
    //

    my.pointerDown = function(event) {
        if (downPointers.length > 0) {
            twoFingerTap(event);
        }

        startX = event.originalEvent.clientX;
        startY = event.originalEvent.clientY;
        lastX = startX;
        lastY = startY;

        downPointers.push(event.pointerId);
    };

    my.pointerMove = function(event) {
        var currentX = event.originalEvent.clientX,
            currentY = event.originalEvent.clientY,
            lastXDiff = currentX - lastX,
            lastYDiff = currentY - lastY;

        lastX = currentX;
        lastY = currentY;
        xDiff = currentX - startX;
        yDiff = currentY - startY;

        // Start moving the pointer when the movement is far enough from
        // the starting tap.
        if (downPointers.length === 1 && event.pointerId === downPointers[0] &&
            Math.abs(xDiff) >= options.maxTapDistance &&
            Math.abs(yDiff) >= options.maxTapDistance) {
            movePointer(lastXDiff, lastYDiff);
        }
    };

    my.pointerUp = function(event) {
        var x = event.originalEvent.clientX,
            y = event.originalEvent.clientY,
            xDiff = x - startX,
            yDiff = y - startY,
            time = new Date().getTime(),
            millisecondsSinceLastTwoTap = time - lastTwoTapTime;

        if (millisecondsSinceLastTwoTap > 300 &&
            downPointers.length === 1 &&
            Math.abs(xDiff) < options.maxTapDistance &&
            Math.abs(yDiff) < options.maxTapDistance) {
            oneFingerTap(event);
        }

        for (var i = 0; i < downPointers.length; ++i) {
            if (downPointers[i] === event.pointerId) {
                downPointers.splice(i, 1);
            }
        }
    };

    //
    // Private methods
    //

    function bindEvents() {
        options.element.bind('pointerdown', function(evt) {
            my.pointerDown(evt);
        });

        options.element.bind('pointermove', function(evt) {
            my.pointerMove(evt);
        });

        options.element.bind('pointerup', function(evt) {
            my.pointerUp(evt);
        });

        options.element.bind('pointerout', function(evt) {
            downPointers = [];
        });

        options.element.bind('pointercancel', function(evt) {
            downPointers = [];
        });
    }

    function oneFingerTap(event) {
        var time = new Date().getTime(),
            double_click = false;

        if (time - lastOneTapTime < 300) {
            double_click = true;
        }
        options.callbacks['onetap'](double_click);
        lastOneTapTime = new Date().getTime();
    }

    function twoFingerTap(event) {
        lastTwoTapTime = new Date().getTime();
        options.callbacks['twotap']();
    }

    function movePointer(xDiff, yDiff) {
        options.callbacks['move'](xDiff, yDiff);
    }

    init();
    return my;
});
