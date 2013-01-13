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


$(window).load(function() {
    var canvasElementId = '#canvas',
        canvasElement = $(canvasElementId),
        canvas = canvasElement[0],

        buttonToggleSleepDisplay = $('#button-toggle-sleep-display'),
        buttonVolumeUp = $('#button-volume-up'),
        buttonVolumeDown = $('#button-volume-down'),
        buttonPreviousTrack = $('#button-previous-track'),
        buttonNextTrack = $('#button-next-track'),
        buttonPlayPause = $('#button-play-pause');

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

    $('body').bind('pointerdown', function(evt) {
        debug('pointergown');
    });

    $('body').bind('mousedown', function() {
        debug('mousedown');
    });

    $('body').bind('touchstart', function() {
        debug('touchstart');
    });

});
