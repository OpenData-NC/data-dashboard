/* The Connection must be constructed with a connected database object */
function Connection(db, data_type) {
    "use strict";

    /* If this constructor is called without the "new" operator, "this" points
     * to the global object. Log a warning and call it correctly. */
    if (false === (this instanceof Connection)) {
        console.log('Warning: constructor called without "new" operator');
//        return new PostsDAO(db);
    }

    var data = db.collection(data_type);
    this.queryData = function(query_obj, callback) {
        data.find(query_obj[0], query_obj[1]).toArray(function(err, docs){
            var records = [];
            if(err) { throw err; }
            docs.forEach(function(doc) {
/*                if(!doc.pdf || doc.pdf === '') {
                    doc.pdf = null;
                }
                else {
*/
                doc.pdf = doc.pdf.replace('/home/vaughn.hagerty/crime-scrapers','http://130.211.132.6');
 //               }
                records.push(doc);
            
            });
            callback(null,records);
        });
    }

}

module.exports.Connection = Connection;
