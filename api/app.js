var express = require('express')
  , app = express() // Web framework to handle routing requests
  , MongoClient = require('mongodb').MongoClient // Driver for connecting to MongoDB
  , routes = require('./routes'); // Routes for our application

MongoClient.connect('mongodb://localhost:27017/crime', function(err, db) {
    "use strict";
    if(err) throw err;
//    db.collection('incidents').findOne( {county: 'New Hanover'}, function(err, doc){
//        console.log(doc);
//    });    // Register our templating engine
//    app.engine('html', cons.swig);
//    app.set('view engine', 'html');
//    app.set('views', __dirname + '/views');

    // Express middleware to populate 'req.cookies' so we can access cookies
//    app.use(express.cookieParser());

    // Express middleware to populate 'req.body' so we can access POST variables
//    app.use(express.bodyParser());

    // Application routes
    routes(app, db);


    app.listen(3000);
    console.log('Express server listening on port 8082');
});

