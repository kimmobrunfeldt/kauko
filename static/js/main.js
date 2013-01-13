// Sends debug data to server, useful when debugging iPad without console.
function debug(data) {
    $.ajax({
        url: "/debug",
        type: "POST",
        data: {data: JSON.stringify(data)},
        dataType: "json",
        async: false
    });
}


// Sends command to server in format: [command, [param1, ..., paramN]]
// args and kwargs are optional.
function sendCommand(command, args, kwargs) {
    if (typeof args === 'undefined') {
        args = [];
    }

    if (typeof kwargs === 'undefined') {
        kwargs = {};
    }

    $.ajax({
        url: "/command",
        type: "POST",
        data: JSON.stringify([command, args, kwargs]),
        dataType: "json",
        async: false
    });
}


function showKeyboard(element, inputKeyboard) {
    element.fadeIn(100, function(){
        inputKeyboard.focus();
    });
}

function hideKeyboard(element, inputKeyboard) {
    element.fadeOut(100);
    inputKeyboard.blur();
}

function showTouchPad(element) {
    element.show();
}

function hideTouchPad(element) {
    element.fadeOut(100);
}


$(window).load(function() {
    var timer,
        buttonToggleSleepDisplay = $('#button-toggle-sleep-display'),
        buttonVolumeUp = $('#button-volume-up'),
        buttonVolumeDown = $('#button-volume-down'),
        buttonPreviousTrack = $('#button-previous-track'),
        buttonNextTrack = $('#button-next-track'),
        buttonPlayPause = $('#button-play-pause'),
        buttonMute = $('#button-mute'),
        buttonKeyboard = $('#button-keyboard'),
        buttonTouchPad = $('#button-touch-pad'),
        buttonCloseKeyboard = $('#button-close-keyboard'),
        buttonCloseTouchPad = $('#button-close-touch-pad'),
        divKeyboard = $('#div-keyboard'),
        divTouchPad = $('#div-touch-pad'),
        inputKeyboard = $('#input-keyboard'),
        buttonFocusInput = $('#button-focus-input');

    buttonToggleSleepDisplay.bind('pointerdown', function() {
        sendCommand('toggle_sleep_display');
    });

    buttonVolumeUp.bind('pointerdown', function() {
        sendCommand('volume_up');
    });

    buttonVolumeDown.bind('pointerdown', function() {
        sendCommand('volume_down');
    });

    buttonPreviousTrack.bind('pointerdown', function() {
        sendCommand('previous_track');
    });

    buttonNextTrack.bind('pointerdown', function() {
        sendCommand('next_track');
    });

    buttonPlayPause.bind('pointerdown', function() {
        sendCommand('play_pause');
    });

    buttonMute.bind('pointerdown', function() {
        sendCommand('toggle_mute');
    });

    buttonKeyboard.bind('pointerdown', function() {
        showKeyboard(divKeyboard, inputKeyboard);
    });

    buttonTouchPad.bind('pointerdown', function() {
        showTouchPad(divTouchPad);
    });

    buttonCloseKeyboard.bind('pointerdown', function() {
        hideKeyboard(divKeyboard, inputKeyboard);
    });

    buttonCloseTouchPad.bind('pointerdown', function() {
        hideTouchPad(divTouchPad);
    });

    inputKeyboard.keypress(function(e) {
        inputKeyboard.val('');

        var character = String.fromCharCode(e.which);
        sendCommand('send_key', [character]);
        clearTimeout(timer);
        timer = setTimeout(function() {
            inputKeyboard.val('');
        }, 700);
    });

    // Capture backspace
    inputKeyboard.keydown(function(e) {
        if (e.keyCode === 8) {
            // Key code 51 means backspace(delete) in apple script.
            sendCommand('send_key', ['51'], {is_key_code: true});
        }
    });

    inputKeyboard.blur(function() {
        var isVisible = inputKeyboard.is(':visible');
        if (isVisible) {
            inputKeyboard.focus();
        }
    });
});
