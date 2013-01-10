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


$(window).load(function() {
    var canvasElementId = '#canvas',
        canvasElement = $(canvasElementId),
        canvas = canvasElement[0],
        chooseMouseButton = $('#choose-mouse'),
        chooseKeyboardButton = $('#choose-keyboard');
});
