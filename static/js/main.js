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
        chooseMouseButton = $('#choose-mouse'),
        chooseKeyboardButton = $('#choose-keyboard');

    chooseMouseButton.bind('click', function() {
        sendCommand('volume_up');
    });

    chooseKeyboardButton.bind('click', function() {
        sendCommand('volume_down');
    });
});
