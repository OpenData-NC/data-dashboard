var Connection = require('../connection').Connection;

/* The ContentHandler must be constructed with a connected db */
function ContentHandler (db, data_type, query_params, res) {
    "use strict";
    var connection = new Connection(db, data_type);
    var group_by = false;
    this.displayData = function(res,query_params,data_type) {
        "use strict";
        var pieces = query_params.split('/');
        var group_by;
//        var geo = false;
        if(pieces[pieces.length - 2] === 'group_by') {
            group_by = pieces[pieces.length - 1];
            pieces = pieces.slice(0,pieces.length - 2);
        }
/*        if(pieces[pieces.length-1] === 'geo') {
            geo = true;
        }
*/
        var query_obj = make_query(pieces, data_type);
        if (!query_obj.length) {
            return false;
        }
        connection.queryData(query_obj, function(err, records){
            show_json(records, data_type, group_by);
        });
        return true;
    }

    function make_query(pieces,data_type) {
        "use strict";
        var query_obj = {}
        , value 
        , key
        , pieces
        , how_many;
        var date_keys = {'incidents': 'date_reported', 'arrests': 'date_occurred'}
        , date_key = date_keys[data_type];
        var fields = {'_id': false, 'agency': true, 'county': true, 'name': true, 'age': true, 'race': true, 'sex': true, 'charge': true, 'category': true,  address: true, pdf: true, lat: true, lon: true, 'reporting_officer': true};
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
    function stats(data_type, records){
        var date_keys = {'incidents': 'date_reported', 'arrests': 'date_occurred'}
        , date_key = date_keys[data_type];
        var all_stats = {};
        var by_days = [];
        var by_officer = {};
        var days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
        days.forEach(function(day){
            by_days[day] = 0;
        });
        var by_address = {};
        records.forEach(function(record){
            by_days[ days[record[date_key].getDay()]]++;
            if(by_address[record['address']]) {
                by_address[record['address']]+=1;
            }
            else {
                if(record['address'] !== ''){
                    by_address[record['address']] = 1;
                }
            }
            if(record['reporting_officer'] !== ''){
                if(by_officer[record['reporting_officer']]) {
                    by_officer[record['reporting_officer']]+=1;
                }
                else {
                    by_officer[record['reporting_officer']] = 1;
                }
            }
        });
        var addresses = [], officers = [], days = [];
        var skips = /address|restricted/i;
        for(var i in by_address){
            var obj = {};
            if(!skips.test(i)){
                obj[i] = by_address[i];
                addresses.push(obj);
            }
        
        }
        for(var i in by_officer){
            var obj = {};
            obj[i] = by_officer[i];
            officers.push(obj);
            
        
        }
        for(var i in by_days) {
            var obj = {};
            obj[i] = by_days[i];
            days.push(obj);
        
        }
        addresses.sort(obj_sorter);
        officers.sort(obj_sorter);

        function obj_sorter(a,b){
            var a_key = Object.keys(a)[0]; 
            var b_key = Object.keys(b)[0];
            if( b[b_key] > a[a_key]) {
                return 1;
            }
            else if( a[a_key] > b[b_key]) {
                return -1;
            }
            return 0;        
        } 
        all_stats['by_day'] = days;
        all_stats['by_address'] = addresses.slice(0,20);
        all_stats['by_officer'] = officers.slice(0,20);
        return all_stats;
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
        json['stats'] = stats(data_type,records);
        res.status(200);
        res.set('Content-Type','Application/JSON');        
        res.send(JSON.stringify(json));        
    }
    function date_format(date){
        return [ (date.getMonth() + 1), date.getDate(), date.getFullYear() ].join('-');
    }

}

module.exports = ContentHandler;
