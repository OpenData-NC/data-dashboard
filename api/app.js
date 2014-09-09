var express = require('express')
  , app = express() // Web framework to handle routing requests
  , MongoClient = require('mongodb').MongoClient // Driver for connecting to MongoDB
  , routes = require('./routes'); // Routes for our application

MongoClient.connect('mongodb://localhost:27017/crime', function(err, db) {
    "use strict";
    if(err) throw err;
    // Application routes
    routes(app, db);


    app.listen(3000);
    console.log('Express server listening on port 3000');
});

