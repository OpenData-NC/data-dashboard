exports.displayWelcomePage = function(req, res) {
	"use strict";
	res.set('Content-Type','Application/JSON');
	var welcome_msg = {'status': 'OK', 'message': 'Welcome to the crime data API. Try using /show_options/incidents or /show_options/arrests to see example queries'};
	res.status(200);
	res.set('Content-Type','Application/JSON');        		
	res.send(JSON.stringify(welcome_msg));
};
