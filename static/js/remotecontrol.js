// Depends from jQuery, because of $.extend.

var RemoteControl = (function(options) {

    /*
    options.element:
        ID of the element which should contain the remote control buttons
        in a grid like format.

    options.buttons:
        Specifies the remote control layout.
        The button grid's size is 3x5, width=3, height=5.

        Looks like:
        [
            [Button, Button, Button],
                ...
            [Button, Button, Button]
        ]

    options.defaultClasses:
        The default CSS classes that are added for a button.

    */

    var defaultOptions = {

    };

    var my = {},
        options = $.extend(true, {}, defaultOptions, options);

    function init() {

    }

    //
    // Public methods
    //

    my.draw = function() {

    };

    //
    // Private methods
    //



    init();
    return my;
});


var Button = (function(options) {

    /*
    options:
        id: Required. Used as button's id.

    If you give for example cssClasses as an option, the default cssClasses
    option("btn-inverse"), will be overridden.
    */

    var defaultOptions = {

        // small, large
        size: "large",

        // You must choose either icon or label.

        // Name of the icon file in static/img/ directory.
        icon: "",

        // Button label.
        label: "",

        // What CSS classes to add along with 'btn' and the size class which
        // is 'btn-small' or 'btn-large' based on size option.
        // Separate with spaces.
        cssClasses: "btn-inverse"
    };

    var my = $.extend(true, {}, defaultOptions, options);
    return my;
});
