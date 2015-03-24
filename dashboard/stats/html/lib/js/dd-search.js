    (function(){
        google.load("visualization", "1", {packages:["table"]});
        var data_formats = {
                    'Total $s sold': format_currency,
                    'Tax value': format_currency,
                    'Date reported': format_date,
                    'Date occurred': format_date,
                    'Sale date': format_date,
                    'Sale price': format_currency,
                    'Count': format_number,
                    'Record ID': format_detail
                };
            //determine the data type
        var heading_types = {
                    'Total $s sold': 'number',
                    'Tax value': 'number',
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
                };
        var county_dir = find_county();
        var county = dd_config[county_dir].county;
        var base_url = location.href;
        $('#dd-county').text(county);
//load the form html and add click event to search button
        $('#dd-form').load('form.html', add_click);
        $('.dd-nav').each(function() {
            $(this).attr('href', '/' + county_dir + '/' + $(this).attr('href'));
        });
        
        check_search();
        
        window.onpopstate = function(e){
            if(e.state){
                document.getElementById('main-content').innerHTML = e.state.html;                
            }
            
        }
        
        function add_click() {
            $('#search').click(function(){
                var query = find_query_params();
                query?query_data(query):error();
            });
        }
        
        function check_search(){
            if(location.href.indexOf('#!') === -1) {
                return false;
            }
            else{
                var pieces = location.href.split('#!');
                base_url = pieces[0];
                query_data(pieces[1]);
            }
        }
        
        function query_data(query) {
            console.log(query);
            $('#data-tables').empty();
            $('#data-tables').html('<h2>Searching ...</h2>');
            $.get(query)
                .done(function(data){
                    console.log(data);
                    show_data(data, query);
                });
            
        }
        function error(){
            $('#data-tables').html('<h4 class="text-danger">Specify at least one search category.</h4>');
            
        }
        function find_query_params() {
            //these need to be formatted to allow multiple values
            var multiples = ['category-type','party-type', 'gender-type'];
            var search_params = {}
                , data_types = [];
            $('.search-item').each(function(i,item){
                if($(item).val() !== '') {
                search_params[$(item).prop('id')] = $(item).val();
                }
            });
            //here's where we format the multiple values
            multiples.forEach(function(multiple_item) {
                var multiple_vals = [];
                $('.' + multiple_item).each(function(i,item){
                    if($(item).is(':checked') || $(item).val() === "picked") {
                        multiple_vals.push($(item).prop('id'));
                    }
                });
                if(multiple_vals.length > 0) {
                    search_params[multiple_item] = multiple_vals.join('~');
                }
            });
            $('.data-type').each(function(i,item){
                if($(item).is(':checked') || $(item).val() === "picked") {
                    data_types.push($(item).prop('id'));
                }
                search_params['data_types'] = data_types.join('-');
            });

            
            return data_types.length === 0?false:build_query(search_params);
//            return has_data_type?build_query(search_params):false;
        }
        
        function build_query(search_params) {
            var query = ['county', county]
                ,base = '/search';
            $.each(search_params, function(key, value) {
                query.push(key);
                query.push(value);
            });
            return [base, query.join('|')].join('/');
            
        }
        function show_data(data, query){
            var have_no_data = true;
            $('#data-tables').empty();
            for (data_type in data.results) {
//                    console.log(data_type);
//                    console.log(data.results[data_type]);
                if(data.results[data_type].data.length > 0) {
                    have_no_data = false;
                    if(data.results[data_type].detail) {
                        build_detail(data_type, data.results[data_type]);
                    }
                    else {
                        build_table(data_type, data.results[data_type]);
                    }
                }
            }
            have_no_data && $('#data-tables').html('<h4>No results found</h4>');
            var stateObj = { html: document.getElementById('main-content').innerHTML};
            var new_url = [base_url, query].join('#!');
            history.pushState(stateObj, "Data Dashboard", new_url);
        }
     
//not used anymore
        function get_county(){
            var county = '';
            $('.county-location').each(function(i,item){
                if($(item).is(':checked')) {
                    county = $(item).data('location');
                }
            });
            if(county === '') { county = 'New Hanover'; }
            return county;
        }
//uses url ad config file to get county        
        function find_county() {
            var county_re = /org\/([^\/]+)\//;
            var county_match = county_re.exec(location.href);
            return county_match[1];        
        }

        function make_items_clickable(data_type){
            $('.dd-detail').unbind('click');
            $('.dd-detail').bind('click', function(){
                build_detail_query($(this).data('key'), $(this).data('source')); 
            });

        }
        
        function build_detail_query(key, data_source) {
            var detail_param = '|detail|1|';
            var search_types = {
                'incidents': 'incidents',
                'accidents': 'traffic-accidents',
                'arrests': 'arrests',
                'citations': 'citations'
                
            }
            var search_url = '/search/county|'
                + county + detail_param + key + '|data_types|' + data_source;
            window.location.replace('#!' + search_url);
            query_data(search_url);
            
            
        }
        
        function build_detail(data_type, data_content){
            var context = {};
            data_content.headings.forEach(function(key, i){
                context[key] = data_content.data[0][i];
            });
            var hb_temp_path = '/lib/templates/' + data_type + '.handlebars';
            $.get(hb_temp_path, function(data) {
                var template = Handlebars.compile(data);
                $('#data-tables').html(template(context));
                
            });
        }
        
        
        function build_table(data_type, data_content, page_size){
            var data_source = data_content.data_source,
                formatted_table_data = format_data(data_content, data_source);
            if(data_type === 'arrests' || data_type === 'incidents' || data_type === 'accidents' || data_type === 'citations') {
                formatted_table_data.data = formatted_table_data.data.map(function(row) { 
//                    row[0] = truncate(row[0], 15);
                    if(row[row.length-1].indexOf('pdf') !== -1) {
                        var pdf_url = row[row.length-1].replace('/home/vaughn.hagerty/crime-scrapers','');
                        row[row.length-1] = '<a href="http://130.211.132.6' + pdf_url + '" target="_blank">Report</a>';
                    }
                    return row; 
                });
            }
//            else { formatted_table_data = data_content.data; }
            
            var rows = $('.row');
            var table_width = ($(rows[0]).width() - 50) + 'px';
            page_size = page_size || 20;
            var data = new google.visualization.DataTable();
            formatted_table_data.headings.forEach( function(heading) {
                var heading_type = heading_types[heading] || 'string';
                data.addColumn(heading_type,heading);
            });
            data.addRows(formatted_table_data.data);
            var options = {page:'enable',pageSize: page_size, allowHtml: true};
            var table_div_id = 'data-table-' + data_type;
            var table_div = '<h2 style="text-transform: capitalize">' + data_type + ': ' + data_content.data.length + ' records</h2><div style="width:100%" id="' + table_div_id + '"></div>';
            $('#data-tables').append(table_div);
            var table = new google.visualization.Table(document.getElementById(table_div_id));
            google.visualization.events.addListener(table, 'ready', function(){
                
                make_items_clickable(data_source);
                google.visualization.events.addListener(table, 'sort', function(){
                    make_items_clickable(data_source);
                });
                google.visualization.events.addListener(table, 'page', function(){
                    make_items_clickable(data_source);
                });
            });
            table.draw(data,options);
        }
        function format_data(data, data_source) {
            var headings = []
                ,rows = []
                ,row
                , heading_indexes = []
                , headings = data.headings.filter(function(h,i) {
    //                if(h === 'lat' || h === 'lon' || h === 'Order' || h === 'Record ID') {
                    if(h === 'lat' || h === 'lon' || h === 'Order') {
                        return false;
                    }
                    else {
                        heading_indexes.push(i);
                        return true;
                    }
                });
            //filter out and format only those rows we'll be displaying (not lat, lon, order or record id)
            data.data.forEach(function(r,i) {
                var row = r.filter(function(d,j){ return heading_indexes.indexOf(j) !== -1; });
                row.forEach( function(d,i) {
                    //format dates or numbers if the heading is in data_formats (see above)
                    //pass the heading and use that to figure out what the query should be
                    row[i] = data_formats[headings[i]]?data_formats[headings[i]](row[i], data_source):row[i];            
                });
                rows.push(row);           
            });
            data.data = rows;
            data.headings = headings;
            return data;
        }

        //data formatting functions
        function format_date(date_string, data_source) {
            var date = new Date(date_string);
            return {v: date, f: date_string};
        }

        function format_currency(number, data_source) {
            return format_number(number, data_source, '$');
        }
        function format_number(number, data_source, currency) {
            var prefix = currency || ''
                , decimal_places = currency?2:0
                , formatted = prefix + number.formatNumber(decimal_places)
            return {v: number, f: formatted };
        }
        
        function format_detail(record_key, data_source) {
            var detail_link = '<span class="dd-detail" data-key="' + record_key.replace(/"/g,'%22') + '" data-source="' + data_source +'">See detail</span>';
            return detail_link;
            
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
            
        function truncate(string,length) {
            string = string.length > length ? string.substr(0,length-1) + ' ...': string;
            return string;
        }
    })();
