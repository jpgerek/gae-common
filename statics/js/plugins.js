// Avoid `console` errors in browsers that lack a console.
(function() {
    var method;
    var noop = function noop() {};
    var methods = [
        'assert', 'clear', 'count', 'debug', 'dir', 'dirxml', 'error',
        'exception', 'group', 'groupCollapsed', 'groupEnd', 'info', 'log',
        'markTimeline', 'profile', 'profileEnd', 'table', 'time', 'timeEnd',
        'timeStamp', 'trace', 'warn'
    ];
    var length = methods.length;
    var console = (window.console = window.console || {});

    while (length--) {
        method = methods[length];

        // Only stub undefined methods.
        if (!console[method]) {
            console[method] = noop;
        }
    }
}());

/**
 * Given a string it asserts the structure of object exists or creates it.
 * It has to be declared before any namespace object.
 */
function namespace( ) {
    var obj = window,
        tok = null,
        name = null;
    for ( var i = 0; i < arguments.length; i = i + 1 ) {
        tok = arguments[i].split('.');
        for ( var j = 0; j < tok.length; j = j + 1) {
            name = tok[j];
            if ( ! ( name in obj ) ) {
                obj[name] = {};
            }
            obj = obj[name];
        }
    }
    return obj;
}

// Place any jQuery/helper plugins in here.


/**
 * Placeholder simulation for IE.
 */

jQuery.placeholder = function() {
    $('[placeholder]').focus(function() {
        var input = $(this);
        if (input.hasClass('placeholder')) {
            input.val('');
            input.removeClass('placeholder');
        }
    }).blur(function() {
            var input = $(this);
            if (input.val() === '') {
                input.addClass('placeholder');
                input.val(input.attr('placeholder'));
            }
        }).blur().parents('form').submit(function() {
            $(this).find('[placeholder]').each(function() {
                var input = $(this);
                if (input.hasClass('placeholder')) {
                    input.val('');
                }
            });
        });

    // Clear input on refresh so that the placeholder class gets added back
    $(window).unload(function() {
        $('[placeholder]').val('');
    });
};

// If using AJAX, call this on all placeholders after submitting to
// return placeholder
jQuery.fn.addPlaceholder = function() {
    return this.each(function() {
        var input = $(this);
        input.addClass('placeholder');
        input.val(input.attr('placeholder'));
    });
};