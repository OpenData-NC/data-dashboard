var Connection = require('../connection').Connection;

/* The ContentHandler must be constructed with a connected db */
function ContentHandler (db, data_type, query_params, res) {
    "use strict";
//    var res = res;
    var connection = new Connection(db, data_type);
    var group_by = false;
    this.displayData = function(res,query_params,data_type) {
        "use strict";
//        console.log(data_type);
        var pieces = query_params.split('/');
        var group_by;
        if(pieces[pieces.length - 2] === 'group_by') {
            group_by = pieces[pieces.length - 1];
            pieces = pieces.slice(0,pieces.length - 2);
        }
        var query_obj = make_query(pieces, data_type);
        if (!query_obj.length) {
            return false;
        }
        connection.queryData(query_obj, function(err, records){
            show_json(records, data_type, group_by);
        });
        return true;
    }

    function make_query(pieces,data_type, geo) {
        "use strict";
        var query_obj = {}
        , value 
        , key
        , pieces
        , how_many;
        var date_keys = {'incidents': 'date_reported', 'arrests': 'date_occurred'}
        , date_key = date_keys[data_type];
//        var fields = {'_id': false, 'agency': true, 'county': true, 'charge': true, 'category': true, lat: true, lon: true, address: true, pdf: true};
        var fields = {'_id': false, 'agency': true, 'county': true, 'charge': true, 'category': true,  address: true, pdf: true};
        if(geo) {
            fields['lat'] = true;
            fields['lon'] = true;
        }
        fields[date_key] = true;
        how_many = pieces.length;

        //must be even number of pieces:
        //pairs of key and value
        //e.g. category/Assaults        
        if(how_many % 2) { return false; }

        for(var i = 0; i < pieces.length; i++){
            if(i % 2) { //second piece is the value
                value = pieces[i];
                if(key === 'start_date' || key === 'end_date') {
                    query_obj[date_key] = query_obj[date_key] || {};
                    value = new Date(value);
                    //date ranges are start date inclusive, but end date exclusive
                    var operator = key === 'start_date' ? '$gte' : '$lt';
                    query_obj[date_key][operator] = value;
                }
                else {
                    query_obj[key] = value;
                }
            }
            else {
                key = pieces[i];
            }
        }
        return [query_obj, fields];
    }
    function group_records(records, group_by) {
        var grouped_records = {};
        records.forEach(function(record) {
            if(grouped_records[record[group_by]]) {
                grouped_records[record[group_by]]++;
            }
            else {
                grouped_records[record[group_by]] = 1;
            }
        });
        return grouped_records;
    
    }
    function format_records(fields, records){
        var google_records = [],
          record_holder;
        records.forEach(function(record){
            record_holder = [];
            fields.forEach(function(field) {
                record_holder.push(record[field]);
            });
            google_records.push(record_holder);
        });
        return google_records;
    
    }
    
    function format_headers(sample_record) {
        var headers = [], item;
        var keys = Object.keys(sample_record);
        keys.forEach(function(key){
            item = {};
            if(sample_record[key] instanceof Date) {
                item[key] = 'datetime';
            }
            else if (typeof sample_record[key] === 'number') {
                item[key] = 'number';
            }
            else {
                item[key] = 'string';
            }
            headers.push(item);
        });
        return headers;
        
    }
    function show_json(records, data_type, group_by, record_type ) {
        "use strict";
        var json = {};
        record_type = record_type || 'records';
        json['status'] = 'OK';
        json['num_records'] = records.length;
        json['data_type'] = data_type;
        json['headers'] = format_headers(records[0]);
        json[record_type] = format_records(Object.keys(records[0]),records);
        if(group_by) {
            json['grouped'] = {};
            json['grouped'][group_by] = group_records(records, group_by);
        }
        
        res.status(200);
        res.set('Content-Type','Application/JSON');        
        res.send(JSON.stringify(json));        
    }
    function date_format(date){
        return [ (date.getMonth() + 1), date.getDate(), date.getFullYear() ].join('-');
    }

}

module.exports = ContentHandler;
