// Sends debug data to server, useful when debugging device without console.
function debug(data) {
    $.ajax({
        url: "/debug",
        type: "POST",
        data: {data: JSON.stringify(data)},
        dataType: "json",
        async: false
    });
}

// Get settings from server in JSON format
function getSettings() {
    var settings;
    $.ajax({
        url: "/settings",
        type: "GET",
        success: function(response) {
            settings = response;
        },
        async: false
    });
    return settings;
}

$(window).load(function() {
    var timer,
        settings = getSettings(),

        // This must be resolved later, because it is added to DOM in
        // remotecontrol.js
        buttonControlLayer = '#button-control-layer',
        buttonCloseControlLayer = $('#button-close-control-layer'),

        divControlLayer = $('#control-layer'),
        divTouchPad = $('#touch-pad'),
        inputKeyboard = $('#input-keyboard'),

        divRemoteControl = $('#remote-control');

    // Setup the remote control button grid.
    var options = {
            element: divRemoteControl,
            buttons: settings.buttons
        },
        remote = new RemoteControl(options);

    // Setup the touchpad in control layer.
    callbacks = {
        'onetap': function(double_click) {
            remote.sendCommand('mouse_click', [], {"double": double_click});
        },
        'twotap': function() {
            remote.sendCommand('mouse_click', [], {button: 2});
        },
        'move': function(xDiff, yDiff) {
            remote.sendCommand('mouse_move', [xDiff, yDiff]);
        }
    };
    touchPad = new TouchPad({element: divTouchPad, callbacks: callbacks});

    // Bind events for control layer.
    $(buttonControlLayer).on('pointerdown', function() {
        divControlLayer.show();
    });

    buttonCloseControlLayer.on('pointerdown', function() {
        divControlLayer.hide();
    });

    inputKeyboard.keypress(function(e) {
        inputKeyboard.val('');

        var character = String.fromCharCode(e.which);
        remote.sendCommand('send_key', [character]);
        clearTimeout(timer);
        timer = setTimeout(function() {
            inputKeyboard.val('');
        }, 700);
    });

    inputKeyboard.keydown(function(e) {
        // Catch backspace and delete.
        if (e.keyCode === 8 || e.keyCode === 46) {
            // ASCII code 8 means backspace.
            remote.sendCommand('send_key', ['8'], {is_ascii: true});
        }
    });
});
