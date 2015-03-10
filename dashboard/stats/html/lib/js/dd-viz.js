(function(){
    //types of google vizualizations we'll use
    var viz_types = {
                'all': 'Table',
                'by category': 'BarChart',
                'by day of week': 'BarChart',
                'by hour of day': 'BarChart',
                'by address': 'Table',
                'by officer': 'Table',
                'lowest 10 scores': 'Table',
                'score distribution': 'ColumnChart',
                'by party': 'Table',
                'total by day': 'ColumnChart',
                'top 10 sellers': 'Table',
                'top 10 buyers': 'Table'
            }

        , viz_colors = ['#a6bddb','#ADCD9E','#8E7098','#F3D469','#E1755F','#7EBEE4']
    //config options for each viz
        , viz_options = {
                'all': {page:"enable",pageSize:8, allowHtml: true}
                , 'by category': {
//              hAxis:{title:"Number"}
                 colors: viz_colors
              , legend: { position: "none" }
              , animation:{
                  duration: 1000,
                  easing: 'out'
                }
                , width: 500
                , height: 500
                , chartArea: {top: 15, left: 100}
    //            , hAxis: {slantedText: true}
    //          , chartArea:{left:20,top:0,width:'50%',height:'75%'}
                
                
            },
                'by day of week': {
//              hAxis:{title:"Number"}
              colors: viz_colors
              , legend: { position: "none" }
              , animation:{
                  duration: 1000,
                  easing: 'out'
                }
                , width: 500
                , height: 250
                , chartArea: {top: 15, left: 75}
    //            , hAxis: {slantedText: true}
    //          , chartArea:{left:20,top:0,width:'50%',height:'75%'}
                
                
            },
                'by hour of day': {
              hAxis:{title:"Hour"}
              , colors: viz_colors
              , legend: { position: "none" }
              , animation:{
                  duration: 1000,
                  easing: 'out'
                }
                , width: 500
                , height: 700
                , chartArea: {top: 15, left: 100}
                , hAxis: {slantedText: true}
    //          , chartArea:{left:20,top:0,width:'50%',height:'75%'}
                
                
            },
                'by address': {page:"enable",pageSize:20, allowHtml: true},
                'by officer': {page:"enable",pageSize:20, allowHtml: true, width: 450},
                'lowest 10 scores': {page:"enable",pageSize:20, allowHtml: true},
                'score distribution': {
              hAxis:{title:"Score"}
              , vAxis: {title: "#"}
              , colors: viz_colors
              , legend: { position: "none" }
              , animation:{
                  duration: 1000,
                  easing: 'out'
                }
                , width: 900
                , height: 400
                , chartArea: {top: 40, left: 100}
     //           , hAxis: {slantedText: true}
    //          , chartArea:{left:20,top:0,width:'50%',height:'75%'}
                
                
            },
                'by party': {page:"enable",pageSize:20, allowHtml: true, width: 230},
                'total by day': {
              hAxis:{title:"Sale date"}
              , vAxis: {title: "$s"}
              , colors: viz_colors
              , legend: { position: "none" }
              , animation:{
                  duration: 1000,
                  easing: 'out'
                }
                , width: 1000
                , height: 400
                , chartArea: {top: 40, left: 100}
//                , hAxis: {slantedText: true}
    //          , chartArea:{left:20,top:0,width:'50%',height:'75%'}
                
                
            },
                'top 10 sellers': {page:"enable",pageSize:20, allowHtml: true},
                'top 10 buyers': {page:"enable",pageSize:20, allowHtml: true}
        
        
        }
    //format display of certain columns
        , data_formats = {
            'Total $s sold': format_currency,
            'Date reported': format_date,
            'Date occurred': format_date,
            'Sale date': format_date,
            'Sale price': format_currency,
            'Count': format_number
        }
    //determine the data type
        , heading_types = {
            'Total $s sold': 'number',
            'Date reported': 'date',
            'Date occurred': 'date',
            'Sale date': 'date',
            'Sale price': 'number',
            'Count': 'number',
            'Order': 'number',
            'ZIP code': 'number',
            'Hour': 'number',
            'Score': 'number',
            'lat': 'number',
            'lon': 'number'
        }
    //Data types are Arrests, Accidents, Incidents, Citations, Real Estate, RR grades and Voter registration
    $('#voter-registration-head').hide();
    google.load("visualization", "1", {packages:["corechart", "table"]});
//    google.setOnLoadCallback(build_all_viz);
    var county = dd_config[find_county()].county;
    $('#dd-county').text(county);
    google.setOnLoadCallback(load_data);
    function load_data(){
        $.getJSON('data/summary.json', function(data) { build_all_viz(data)} );
        
    }
    function build_all_viz(all_data) {
//    function build_all_viz() {
        $('#dd-loading').remove();
        var has_data;
        for(data_type in all_data) {
            var range = ''
                , has_no_data = true //if we don't have data for a data type, we'll delete that div
                , main_data_type;
            //summary types include both "all" and summary data such as "by day", etc.
            for(summary_type in all_data[data_type]) {
 
                var main_data_type = data_type.toLowerCase().replace(/ /g,'-'); //id for data type div
                if(all_data[data_type][summary_type].data.rows.length === 0) { continue; }
                else { has_no_data = false; } 
                //determine the viz type we want, the div where it'll be placed and options
                //then draw it.
                var div = append_div(data_type, summary_type) //div for this viz
                    , viz_type = viz_types[summary_type] //type of viz (table, line chart or column chart
                    , viz_option = viz_options[summary_type]; //options for this div
                if(all_data[data_type][summary_type]["date ranges"] && range === '') {
//                    main_data_type = data_type.toLowerCase().replace(/ /g,'-');
                    var main_heading = '<h2 class="dd-upper">' + data_type + '</h2>';
                    $('#' + main_data_type).prepend(main_heading);
                    range = '<h4>Data from ' + all_data[data_type][summary_type]["date ranges"].start + ' to ' + all_data[data_type][summary_type]["date ranges"].end  + '</h4>';
                }
                draw_viz(all_data[data_type][summary_type].data, viz_type, div, viz_option);
                //here maybe we can add the data ranges we're using for each one
            }
            if(main_data_type !== 'voter-registration') { $('#' + main_data_type + ' h2:first').after(range);}
            if(has_no_data) {
                $('#' + main_data_type).remove();
            }
        }
        $('.row').addClass('main-data-cat'); //puts borders around specific data types
//        $('.health-insp').addClass('health-insp-cat'); //horizontal line between health insp and voter data
        $('#voter-registration-head').show();
    }
    //appends the div to hold the viz and returns its id
    function append_div(data_type, summary_type) {
        var main_data_type = data_type.toLowerCase().replace(/ /g,'-')
            , sub_type = summary_type.toLowerCase().replace(/ /g,'-')
            , div_id = [main_data_type, sub_type].join('-')
            , div = ['<div id="', div_id, '"></div>'].join('')
            , heading = ['<h4 class="dd-cap">', summary_type, '</h4>'].join('');
        $('#' + div_id).before(heading);
//        $('#' + main_data_type).append(div);
        return div_id;
    }

    function draw_viz(data, viz_type, div, options) {
        var viz_data = make_viz_data(data);
        if(viz_type) {
            var viz = new google.visualization[viz_type](document.getElementById(div));
            viz.draw(viz_data,options);
        }
    }

    function make_viz_data(data) {
        var formatted_data = format_data(data)
            , headings = formatted_data.headings
            , viz_data = new google.visualization.DataTable();
        headings.forEach(function(h,i) {
            heading_type = heading_types[h] || 'string';
            viz_data.addColumn(heading_type, h);
        });
        viz_data.addRows(formatted_data.rows);
        return viz_data;
    }

    function format_data(data) {
        var headings = []
            ,rows = []
            ,row
            , heading_indexes = []
            , headings = data.headings.filter(function(h,i) {
                if(h === 'lat' || h === 'lon' || h === 'Order' || h === 'Record ID') {
                    return false;
                }
                else {
                    heading_indexes.push(i);
                    return true;
                }
            });
        //filter out and format only those rows we'll be displaying (not lat, lon, order or record id)
        data.rows.forEach(function(r,i) {
            var row = r.filter(function(d,j){ return heading_indexes.indexOf(j) !== -1; });
            row.forEach( function(d,i) {
                //format dates or numbers if the heading is in data_formats (see above)
                row[i] = data_formats[headings[i]]?data_formats[headings[i]](row[i]):row[i];            
            });
            rows.push(row);           
        });
        data.rows = rows;
        data.headings = headings;
        return data;
    }

    //data formatting functions
    function format_date(date_string) {
        var date = new Date(date_string);
        return {v: date, f: date_string};
    }

    function format_currency(number) {
        return format_number(number, '$');
    }
    function format_number(number, currency) {
        var prefix = currency || ''
            , decimal_places = currency?2:0
            , formatted = prefix + number.formatNumber(decimal_places)
        return {v: number, f: formatted };
    }
    
    function find_county() {
        var county_re = /org\/([^\/]+)\//;
        var county_match = county_re.exec(location.href);
        return county_match[1];        
    }
    //from stack overflow
    function toTitleCase(str) {
        return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
    }

    Number.prototype.formatNumber = function (c, d, t) {
        var decimal_places = 2;    
        var n = this,
            c = isNaN(c = Math.abs(c)) ? 2 : c,
            d = d == undefined ? "." : d,
            t = t == undefined ? "," : t,
            s = n < 0 ? "-" : "",
            i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + "",
            j = (j = i.length) > 3 ? j % 3 : 0;
        return s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
    };
})();
