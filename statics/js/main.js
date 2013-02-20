!function(window, document, undefined) {
    var me = namespace('App');

    me.trackPageView = function (url) {
        if ('_gaq' in window) {
            _gaq.push(['_trackPageview', url]);
        }
    };
}(window, document);
