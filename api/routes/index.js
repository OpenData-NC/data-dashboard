var ContentHandler = require('./content')
  , ErrorHandler = require('./error').errorHandler
  , Welcome = require('./welcome');

module.exports = exports = function(app, db) {


    app.get('/', Welcome.displayWelcomePage);

    // our requests
    app.get(/\/([^\/]+)\/(.+)$/, function(req, res, next) {
        var query_params = req.params[1]
          , data_type = req.params[0];
        //TODO: add whitelisting to restrict collections
        //and poss query types
        var contentHandler = new ContentHandler(db, data_type, query_params, res);
        //show available data types and sample queries
        if(query_params === 'show_options') {
            contentHandler.showAvailableOptions;
        }
        //show actual data
        else {
            contentHandler.displayData(res,query_params,data_type);
//            contentHandler.displayData() || app.use(ErrorHandler);           
        }
    });

    // Error handling middleware
    //app.use(ErrorHandler);
    
}
