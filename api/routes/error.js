// Error handling middleware

exports.errorHandler = function(err, req, res, next) {
    "use strict";
    var err_msg = {'status': 'Error', 'message': 'We did\'nt understand your request. Try using /show_options/incidents or /show_options/arrests to see example queries'};
    res.status(404);
    res.set('Content-Type','Application/JSON');
    res.send(err_msg);
}
