    (function(){
        google.load("visualization", "1", {packages:["corechart","table"]});
//widget configs
        var graph_configs = {}
            , which_graph
            
            , table_options = {page:"enable",pageSize:8, allowHtml: true, width: 700};
        
        var data_formats = {
                    'Total $s sold': format_currency,
                    'Tax value': format_currency,
                    'Date reported': format_date,
                    'Date occurred': format_date,
                    'Sale date': format_date,
                    'Sale price': format_currency,
                    'Count': format_number,
                    'Record ID': format_detail,
                    'REAL-ASSVAL': format_currency_detail,
                    'LAND-ASSVAL': format_currency_detail,
                    'EXFEAT-ASSVAL': format_currency_detail,
                    'BLDG-ASSVAL': format_currency_detail,
                    'USE-ASSVAL': format_currency_detail,
                    'APP-LAND-VAL': format_currency_detail,
                    'APP-FEAT-VAL': format_currency_detail,
                    'APP-BLDG-VAL': format_currency_detail,
                    
                    'TaxableVal': format_currency_detail,
                    'LandMarket': format_currency_detail,
                    'BldgMarket': format_currency_detail,
                    'ImprMarket': format_currency_detail,
                    'DfrdMarket': format_currency_detail,
                    'DeedDate': format_date_detail,
                    'SellingPrice': format_currency_detail,
                    'SellDate': format_date_detail,
                    'price': format_currency_detail,
                    'sale_date': format_date_detail,
                    'BUILDING_ASSESSED_VALUE': format_currency_detail,
                    'LAND_ASSESSED_VALUE': format_currency_detail,
                    'TOTAL_SALE_PRICE': format_currency_detail,
                    'LAND_SALE_PRICE': format_currency_detail,
                    'LAND_DEF_AMOUNT': format_currency_detail,
                    'TOT_SCH_VAL_ASSD': format_currency_detail,
                    'TOTAL_SALE_DATE': format_date_detail,
                    'LAND_SALE_DATE': format_date_detail,
                    'DEED_DATE': format_date_detail,
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

        if(get_cookie('dd-email')) {
            show_manage_user();
        }
        else {
            show_log_in();
        }
        
        check_search();
        
        window.onpopstate = function(e){
            if(e.state){
                document.getElementById('main-content').innerHTML = e.state.html;
                make_items_clickable();
            }
            else {
                $('#data-tables').empty();
                add_click();
            }
        }
        
        
        function show_manage_user(){
            var manage_user = fill_template('user-management',{});
            $('#dd-log-in-menu').remove();
            $('.navbar-nav').append(manage_user);
            $('#dd-manage-alerts').click( function(e) {
                show_manage_alerts();
            });
            $('#dd-log-out').click( function(e) {
                set_cookie('dd-email','', -100);
                show_log_in();
            });
        }
        
        function show_manage_alerts() {

            $('#alert-modify-modal').remove();
            var email = get_cookie('dd-email');
            manage_alerts_data(email, false);
        }

        function manage_alerts_data(email, is_refresh){
            var alerts_url = '/search/users/type|show-alerts|email|' + email;
            $.get(alerts_url)
                .done(function(data){ 
                    if(is_refresh) {
                        var table_html = fill_template('show-alerts-updated',data);
                        $('#show-alerts-body').html(table_html);
                        manage_alerts_click(email);
                        
                    }
                    else {
                        var modal_html = fill_template('show-alerts-modal',data);
                        $('#data-tables').prepend(modal_html);
                        $('#alert-modify-modal').modal();
                        manage_alerts_click(email);
                    }
                    
                })
            
        }
        
        function manage_alerts_click(email) {
            $('#modify-alert').click( function(e) {
                e.preventDefault();
                var alert_details = [];
                $('.show-dash-alerts').each( function(i, el) {
                    var this_alert = [];
                    var changed = false;
                    $(el).children('td').children('input').each(function(j, ch) {
                    
                        var this_value = 0;
                        var data_field = $(ch).attr('class');
                        if($(ch).is(':checkbox')){
                            if($(ch).is(':checked')) {
                                if(data_field === 'alert-pause') {
                                    if($(ch).val() == 0) {
                                        changed = true;
                                    }
                                }
                                else {
                                    changed = true;
                                }
                                this_value = 1;
                            }
                            else {
                                if(data_field === 'alert-pause') {
                                    if($(ch).val() == 1) {
                                        changed = true;
                                    }
                                }
                            }
                        }
                        else {
                            this_value = $(ch).val().replace(/\|/g,'*');
                        }

                        var this_field = data_field + '|' + this_value;
                        this_alert.push(this_field);
                    
                    });
                    if(changed) {
                        this_alert.push('email', email);
                        alert_details.push(this_alert.join('|'));
                    }
                });
                if(alert_details.length > 0) {
                    modify_alerts(alert_details.join('~'), email);
                }
                else {
                    var msg = "No changes made. If you're done, click Cancel. Or make a change.";
                    $('#modify-msg').text(msg);
                }
            });
            
        }
        
        function modify_alerts(alerts, email) {
            var modify_url = '/search/modify/' + alerts.replace(/\//g, '}');
            console.log(modify_url);
            $.get(modify_url)
                .done(function(data) {
                    $('#modify-msg').text(data.alerts_modified);
                    manage_alerts_data(email, true);
                });
            
        }
        
        function show_log_in() {
            var log_in_user = fill_template('log-in',{});
            $('#dd-manage-user').remove();
            $('.navbar-nav').append(log_in_user);
            $('#dd-log-in').click(function(e) {
               show_login_register(); 
            });
            
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
        
        function allowed_alert(query) {
            var filtered_alert = [];
            var not_allowed = ['voter','health','property','realestate'];
            var pieces = query.split('|');
            var data_types = pieces.pop().split('-');
            var allowed = data_types.filter( function(data_type) {
                return not_allowed.indexOf(data_type) === -1;
            });
            if(allowed.length === 0) {
                return false;
            }
            else {
                pieces.push(allowed.join('-'));
                return pieces.join('|');
                
            }
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
            //only crime data for now
            var not_last_searched = true;
            if(query.indexOf('last-searched') !== -1) {
                not_last_searched = false;
            }
            var filtered_query = allowed_alert(query);
            if(not_last_searched && filtered_query) {
                var query_btn_text = '';
                if(filtered_query != query) {
                    query_btn_text = ' (only crime data will be used)';
                }
                $('#data-tables').prepend('<button type="button" style="margin-bottom: 1em" class="btn-default btn" id="dd-save-query" data-query="' + filtered_query + '">Create an alert with this search</button>' + query_btn_text);
            }
            $('#dd-save-query').click(function(e) {
                e.preventDefault();
                var query = $(this).data('query');
                create_alert(query);
            });
        }

        function create_alert(query) {
            query = query.replace('search/','search/alerts/');
            var today = new Date();
            today = [today.getFullYear(),(today.getMonth()+1),today.getDate()].join('-');
            console.log(query + ['|','last-searched','|',today].join(''));
            
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
                'citations': 'citations',
                'rr': 'health-inspections',
                'dash_nh_rr': 'health-inspections',
                'nc_voters_new': 'voter-registration',
                'dash_nh_property': 'property-tax',
                'dash_nh_real_estate': 'real-estate',
                'dash_buncombe_property': 'property-tax',
                'dash_buncombe_real_estate': 'real-estate',
                'dash_wake_property': 'property-tax',
                'dash_wake_real_estate': 'real-estate',
                
            }
            var search_url = '/search/county|'
                + county + detail_param + key + '|data_types|' + data_source;
//            window.location.replace('#!' + search_url);
            query_data(search_url);
            
        }
        

        
        function build_detail(data_type, data_content){
            var context = {};
            data_content.headings.forEach(function(key, i){
                context[key] = data_formats[key]? data_formats[key](data_content.data[0][i]): data_content.data[0][i];
            });
            var hb_temp_path = '/lib/templates/' + data_type + '.handlebars';
            $.get(hb_temp_path, function(data) {
                var template = Handlebars.compile(data);
                $('#data-tables').html(template(context));
                
            });
        }
        
        
        function build_table(data_type, data_content, page_size){
            var data_source = data_content.data_source,
                formatted_table_data = format_data(data_content, data_source),
                table_data_holder = {};
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
            var viz_click_btn = table_div_id + '-btn';
            var table_div = '<div><h2 style="text-transform: capitalize; display:inline">' + data_type.replace('estate',' estate') + ': ' + data_content.data.length + ' records</h2> <button type="button" style="margin-left: 3em; margin-bottom: 1em;" id="' + viz_click_btn + '" class="btn btn-default" data-which="' + table_div_id + '">Create visualization</button></div><div style="width:100%" id="' + table_div_id + '"></div>';
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
            table_data_holder[table_div_id] = data;
            table.draw(data,options);
            
            $('#' + viz_click_btn).click(function(e) {
                e.preventDefault();
                var which_data = $(this).data('which');
                var data = table_data_holder[which_data];
                show_widget_wizard(data.toJSON(), data_type, county);
            });
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
        
        //alert stuff starts here
        function create_alert(query) {
            var email = get_cookie('dd-email');
            if(!email) {
                show_login_register(query);
            }
            else {
                add_alert(email, query);
            }
        }
        function show_login_register(query){
            var query = query || 'none';
            $('#login-register-modal').remove();
            var modal_html = fill_template('login-register-modal',{'alert-query': query});
            $('#data-tables').prepend(modal_html);
            $('#login-register-modal').modal();
            $('#login-registered').click(function(e) {
                e.preventDefault();
                login_registered();
            });
            $('#register-user').click(function(e) {
                e.preventDefault();
                login_registered(true);
            });
        }
        function login_registered(is_registration) {
            var type, name, pass, phone, user, params, msg;
            if(is_registration) {
                user = $('#new-user-email').val();
                pass = $('#new-user-password').val();
                name = $('#new-user-name').val();
                phone = $('#new-user-phone').val();
                params = ['type', 'register', 'user', user, 'password', pass, 'name', name, 'phone', phone];
                
            }
            else { //we're logging in
                user = $('#registered-user-email').val();
                pass = $('#registered-user-password').val();
                params = ['type', 'login', 'user', user, 'password', pass];
                
            }
            var query = $('#alert-query').val();
            var url = '/search/users/' + params.join("|");
            console.log(url);
            $.get(url)
                .done(function(data) {
                    console.log(data);
                    if(data.success == 'no') {
                        if(is_registration) {
                            msg = 'That email is already registered. Please log in or create a new account';
                        }
                        else {
                            msg = 'Username and/or password incorrect';
                        }
                        $('#alert-msg').text(msg).addClass('text-warning');
                    }
                    else {
                        set_cookie('dd-email',user);
                        if(query !== 'none') {
                            add_alert(user, query, true);
                        }
                        //just logging in
                        else {
                            $('#login-register-modal').modal('hide');
                        }
                        $('.dd-log-in').remove();
                        show_manage_user();
                    }
                });
        }
        function add_alert(email, query, is_modal) {
            query+= '|user|' + email;
            query = query.replace('/search/','/search/alerts/');
            console.log(query);
            $.get(query)
                .done(function(data){
                    console.log(data);
                    show_query_added(data, is_modal);
                });
            
        }

        function show_query_added(data, is_modal) {
            var msg = data.alert_result;
            $('#dd-alert-msg').remove();
            if(data.success === 'no') {
                if(is_modal) {
                    $('#alert-msg').text(msg).addClass('text-warning');
                }
                else {
                    msg = '<h4 id="dd-alert-msg">' + msg + '</h4>';
                    $('#dd-save-query').after(msg);
                }
            }
            else {
                if(is_modal) {
                    $('#login-register-modal').modal('hide');
                }
                msg = '<h4 id="dd-alert-msg">This alert has been added. Any new records we collect matching this search will be sent to your email beginning tomorrow.</h4>';
                $('#dd-save-query').after(msg);
                $('#dd-save-query').remove();
                }
        }
        
        function set_cookie(name, val, expire_days) {
            expire_days = expire_days || 1000;
            var d = new Date();
            d.setTime(d.getTime() + (expire_days * 24 * 60 * 60 *1000));
            var cook_params = [name,val].join('=');
            console.log(d.toUTCString());
            var exp_params = ['expires',d.toUTCString()].join('=');
            document.cookie = [cook_params,exp_params,'path=/'].join(';');
        }

        function get_cookie(name) {
            var pattern = new RegExp(name + '=([^;]+)');
            var val = pattern.exec(document.cookie);
            return val?val[1]: false;
        }
        //alert stuff ends here
        
        
        //widget stuff starts here
        function hide_widget_wizard() {
            $('#open-nc-widget').remove();
            $('#dd-form, #data-tables').show('slow');            
        }
        function show_widget_wizard(data, data_type, county) {
            $('#dd-form, #data-tables').hide('slow')
            $('#dd-form').before('<div id="open-nc-widget" style="width: 600px"><button type="button" class="btn btn-default" id="hide-widget-wizard">Back to search results</div>');
            $('#hide-widget-wizard').click( function(e) {
                hide_widget_wizard();
            });
            show_available_graphs(JSON.parse(data), data_type, county);
        }

        function show_available_graphs(table_data, data_type, county) {
//            console.log(table_data);
                
            var skip_labels = ['Record ID', 'View report']
                , skip_labels_table = ['Record ID']
                , headings = []
                , table_headings = []
                , skip_indexes = []
                , too_many = []
                , data_and_msg
                , graph_type;
            //table stuff here    
            table_data.cols.forEach(function(col, index) {
                if(skip_labels.indexOf(col.label) < 0) {
                    headings.push({label:col.label, index: index});
    //                group_on({label:col.label, index: index});
                }
                if (skip_labels_table.indexOf(col.label) < 0){
                   table_headings.push(col);
                }
                else {
                    skip_indexes.push(index);
                }
            });
            headings.forEach(function(heading) {
                data_and_msg = group_on(heading.label, data_type, headings, table_data.rows);
                
                if(data_and_msg['msg']) {
                    too_many.push(data_and_msg['msg']);
                }

            });
            var source = find_source(county, data_type, headings, table_data.rows);
            make_table(table_data, table_headings, skip_indexes);
            if(too_many.length > 0) {
                var msg = '<div class="dd-graphs"><p><b>The following fields have too many unique values to reasonably graph:</b></p>' + too_many.join("\n") + '</div>';
                $('#open-nc-widget').append(msg);

            }


            //pull out into own function
            $('.graph-option').click(function() {
                which_graph = $(this).data('which');
                var graph_config = graph_configs[which_graph];
    //            console.log(graph_config);
                $('.dd-graphs').each(function(index, el) {
                    if($(this).attr('id') !== ('holder-' + which_graph)) {
                        $(this).hide('slow');
                    }
                });
                $(this).after('<button class="btn btn-default graph-show-all">Back to all graphs</button>');
                $(this).hide();
                $('.graph-show-all').after(' <button class="btn btn-default graph-show-code" style"margin-left: 5px">Get code</button>');
                $('.graph-show-code').click(function(e) {
                    e.preventDefault();
                    var graph_type = graph_config['graph_type'];
                    var output_template = '_graph';
                    var height = parseInt($('#graph-height').val()) || 'auto';
                    var width = parseInt($('#graph-width').val());
                    var context = {width: width, height: height, source: source, data: JSON.stringify(graph_config['data']), options: JSON.stringify(graph_config['options']), viz_type: graph_type ,script: 'script'};
                    if(graph_type !== 'Table'){
                        context['array_to'] = 'arrayTo';
                    }
                    else {
                        context['view'] = JSON.stringify(graph_config.view);
                        output_template = '_table';
                        
                    }
                    var code = fill_template('embed_output' + output_template,context);
                    var embed_textarea = fill_template('embed_textarea',{});
                    $('#' + which_graph).before(embed_textarea);
                    $('#embed-code').val(code);
                    $('#embed-code').on('click',function() {
                        this.select();
                    });
                });
                $('.graph-show-all').click( function(e) {
                    e.preventDefault();
                    if(graph_type !== graph_config['graph_type']) {
                        graph_type = graph_config['graph_type'];
    //                    show_graph(graph_config['data'],which_graph,graph_config['options'], graph_type);
                        show_graph(graph_config,which_graph);
                    }
                    $('#embed-code-row, .widget-form, .graph-show-code').remove();                
                    $('.dd-graphs').show('slow');
                    $(this).remove();
                    $('.graph-option').show();
                    $('#graph-change-form').remove();
                });

                //own function
                //puts existing values in form
                var form_template = 'graph_widget_form';
                var context = {};
                if(graph_config['graph_type'] === 'Table') {
                    form_template = 'table_widget_form';
                    context['headings'] = graph_config['headings'];
                }
                var form = fill_template(form_template, context);
                $('#holder-' + which_graph).append(form);
                if(graph_config['graph_type'] === 'LineChart') {
                    $('#graph-change-row').remove();
                }
                $('.graph-change-param').each(function(i, el) {
                    var param = $(this).data('option');
                    var form_type = $(this).attr('type');
                    var val;
                    if(param.indexOf('.') !== -1) {
                        var keys = param.split('.');
                        var val_obj = graph_config['options'];
                        keys.forEach( function(key) {
                            val_obj = val_obj[key];
                        });
                        val = val_obj;
                    }
                    else {
                        if(param === 'colors') {
                            val = graph_config['options'][param][0];
                        }
                        else {
                            val = graph_config['options'][param];   
                        }
                    }
                    if(form_type === 'radio' || form_type === 'checkbox') {
                        if($(this).val() === val) {
                            $(this).attr('checked','checked');
                        }
                        
                    }
                    else {
                        $(this).val(val);
                    }
                });
                $('.graph-type').click( function() {
                    graph_type = $(this).val();
                    var temp_config = graph_config;
                    graph_config['graph_type'] = graph_type;
    //                show_graph(graph_config['data'],which_graph,graph_config['options'], graph_type);
                    show_graph(graph_config,which_graph);
                });
                //puts form values in option obj
                $('#graph-change-button').click( function(e) {
                    e.preventDefault();
                    $('.graph-change-param').each( function(i, el) {
                        var data_type = $(el).attr('type');
                        if(data_type === 'number') {
                            val = parseInt($(el).val());
                        }
                        else if (data_type === 'radio' || data_type === 'checkbox') {
                            if($(el).is(':checked')) {
                                val = $(el).val();
                            }
                        }
                        else {
                            val = $(el).val();
                        }
                        var param = $(el).data('option');
                        if(param === 'hAxis.title' && val !== '' && val && (graph_config['graph_type'] === 'ColumnChart' || graph_config['graph_type'] === 'LineChart')) {
                            graph_config['data'][0][1] = val;
                        }
                        if(param === 'vAxis.title' && val !== '' && val && graph_config['graph_type'] === 'BarChart') {
                            graph_config['data'][0][1] = val;
                        }
                        if(param.indexOf('.') !== -1) {
                            var keys = param.split('.');
                            var val_obj = {};
                            var last = keys.length;
                            var first = keys[0];
                            for(var i = 1; i < keys.length; i++) {
                                val_obj[keys[i]] = val;
                            }
                            graph_config['options'][first] = val_obj;
                        }
                        else {
                            if(param === 'colors') {
                                if(graph_config['options']['colors'][0] !== val) {
                                    
                                    graph_config['options']['colors'].unshift(val);
                                }
                            }
                            else {
                                graph_config['options'][param] = val;   
                            }
                        }
                        
                    });
                    if(graph_config['graph_type'] === 'Table') {
                        var show_cols = [];
                        $('.table-fields').each(function(i, el) {
                            if($(el).is(':checked')) {
                                show_cols.push(parseInt($(el).val()));
                            }
                        });
                        graph_config['view'] = show_cols;
                    }
    //                show_graph(graph_config['data'],which_graph,graph_config['options'], graph_config['graph_type'], graph_config['view']);
                    show_graph(graph_config,which_graph);
                    $('#embed-code-row').remove();                
                });
                $('#graph-change-reset').click(function(e) {
                    e.preventDefault();
                    $('.graph-change-param').each(function(i, el) {
                        var param = $(this).data('option');
                        var form_type = $(this).attr('type');
                        var val;
                        if(param.indexOf('.') !== -1) {
                            var keys = param.split('.');
                            var val_obj = graph_config['options'];
                            keys.forEach( function(key) {
                                val_obj = val_obj[key];
                            });
                            val = val_obj;
                        }
                        else {
                            if(param === 'colors') {
                                val = graph_config['options'][param][0];
                            }
                            else {
                                val = graph_config['options'][param];   
                            }
                        }
                        if(form_type === 'radio' || form_type === 'checkbox') {
                            if($(this).val() === val) {
                                $(this).prop('checked',true);
                            }
                            else {
                                $(this).prop('checked', false);
                            }
                            
                        }
                        else {
                            $(this).val(val);
                        }
                        if(graph_type !== 'ColumnChart') {
                            graph_type = 'ColumnChart';
    //                        show_graph(graph_config['data'],which_graph,graph_config['options'], graph_type);
                            show_graph(graph_config,which_graph);
                        }
                    });                
                });
            });
        }
        
        function find_source(county, data_type, headings, data){
            var crime = ['incidents', 'arrests', 'accidents', 'citations']
                , agencyIndex
                , source;
            var others = {
                'realestate': ' County Tax Office',
                'property': ' County Tax Office',
                'health': ' County Health Department',
                'voter': 'N.C. Board of Elections'
            }
            if (crime.indexOf(data_type) !== -1) {
                headings.forEach(function(heading) {
                    if(heading.label === 'Agency') {
                        agencyIndex = heading.index;
                    }
                    
                });
                var agencies = [];
                data.forEach(function(row) {
                    if (agencies.indexOf(row.c[agencyIndex].v) < 0) {
                        agencies.push(row.c[agencyIndex].v);
                    }
                });
                source = agencies.sort().join(", ");
            }
            else {
                source = county.toUpperCase() + others['data_type'];
            }
            return source;
        }

        function fill_template(id,context) {
            var hb_temp_path = '/lib/templates/' + id + '.handlebars';
            var compiled_temp = null;
            $.ajax({
                url: hb_temp_path,
                type: 'get',
                dataType: 'html',
                async: false,
                success: function(data) {
                    result = data;
                    compiled_temp = Handlebars.compile(data);
                }
            });
            return compiled_temp(context);

        } 
        
        //group_on('Category', headings, table_data.rows);
        //show headings to pick
        function group_on(field, data_type, headings, data, options) {
            var index = index_wanted(field, headings)
    //            , date_labels = ['Date occurred', 'Date reported', 'Sale date', 'Insp. date']
                , date_labels = []
                , grouped = {}
                , grouped_array = [[field,"Count"]]
                , msg
                , max = 50;
                var options = options || init_options(field, data_type);
            data.forEach(function(row) {
                var val = row.c[index].f || row.c[index].v;
                if(!grouped[val]) { grouped[val] = 0}
                grouped[val]++;
            });
            $.each(grouped, function(heading, count) {
                grouped_array.push([heading, count]);
            });
            var graph_div = 'graph-div-' + index;
            var graph_holder = 'holder-' + graph_div;
            var graph_type = date_labels.indexOf(field) !== -1 ? 'LineChart' : 'ColumnChart';
            var how_many = grouped_array.length - 1;
            if(how_many > max && graph_type === 'ColumnChart') {
                msg = '<p>' + field + ' (' + how_many + ')</p>';
            }
            else {
                $('#open-nc-widget').append('<div id="' + graph_holder + '" class="dd-graphs"></div>');
                $('#' + graph_holder).append('<div id="' + graph_div + '" class="dd-graph-div"></div>');
                graph_configs[graph_div] = {'data': grouped_array, 'options': options, 'graph_type': graph_type};
                show_graph(graph_configs[graph_div],graph_div);
                $('#' + graph_holder).prepend('<button class="btn btn-default graph-option" data-which="' + graph_div + '">Customize</button>');
    //            console.log(JSON.stringify(grouped_array));
            }
            return {'data': grouped_array, 'msg': msg, 'div': graph_div};
        }
        function make_table(table_data, table_headings, skip_indexes){
            var table_data_rows = table_data.rows.map( function(row) {
                var new_row = [];
                row.c.forEach(function (data, index) {
                    if(skip_indexes.indexOf(index) === -1){
                        new_row.push(data);
                    }
                    row['c'] = new_row;
                });
                return row;
            });
            var filtered_table_data = {cols: table_headings, rows: table_data_rows};
            var headings = []
                ,view = [];
            table_headings.forEach( function(heading,index) {
                headings.push({label: heading.label, index: index});
                view.push(index);
            });
            var table_div = 'table-div-1';
            var table_holder = 'holder-' + table_div;
            $('#open-nc-widget').append('<div id="' + table_holder + '" class="dd-graphs"></div>');
            $('#' + table_holder).append('<div id="' + table_div + '" class="dd-graph-div"></div>');
            $('#' + table_holder).prepend('<button class="btn btn-default graph-option" data-which="' + table_div + '">Customize</button>');
            graph_configs[table_div] = {'data': filtered_table_data, 'options': table_options, 'graph_type': 'Table', 'headings': headings,'view':view};        
    //        show_graph(filtered_table_data, table_div, table_options, 'Table');
            show_graph(graph_configs[table_div],table_div);
        }
        function init_options(field, data_type) {
            var colors = ['#ADCD9E','#8E7098','#F3D469','#E1755F','#7EBEE4'];
            var options = {
                title: capitalizeFirstLetter(data_type) + ' by ' + field.toLowerCase(), 
                width: 700,
                height: 400,
                legend: { position: 'right' },
                colors: colors,
                hAxis: {title: '', minValue: 0},
                vAxis: {title: '', minValue: 0},
                curveType: 'function',
                animation: {startup: true, easing: 'linear'}
            };
            return options;
        }

    //    function show_graph(graph_data, graph_div, options, graph_type, view) {
        function show_graph(graph_config, graph_div) {
    //        console.log(graph_config);
            var graph_type = graph_config.graph_type || "ColumnChart";
            if(graph_type === 'Table') {
                var data = new google.visualization.DataTable(graph_config.data);
                data = new google.visualization.DataView(data);
                if(graph_config.view) {
                    data.setColumns(graph_config.view);
                }
            }
            else {
                var data = new google.visualization.arrayToDataTable(graph_config.data);
            }
            var chart = new google.visualization[graph_type](document.getElementById(graph_div));
            chart.draw(data, graph_config.options);
            
        }
        
        function index_wanted(field, headings) {
            var index;
            headings.forEach( function(heading) {
                if(heading.label === field) {
                    index = heading.index;
                }
            });
            return index;
            
        }
        //from StackOverflow
        function capitalizeFirstLetter(string) {
            return string.charAt(0).toUpperCase() + string.slice(1);
        }            
        //widget stuff ends here

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

        function format_currency_detail(number) {
            return format_number_detail(number, '$');
        }
        function format_number_detail(number, currency) {
            if(typeof number !== 'number') {
                try {
                    number = parseFloat(a);
                }
                catch(err) {
                    return 'Cannot format ' + number;
                }
            }
            var prefix = currency || ''
                , decimal_places = currency?2:0
                , formatted = prefix + number.formatNumber(decimal_places)
            return formatted;           
        }
        function format_date_detail(date_string) {
            var d = new Date(date_string + 'T00:00:00-05:00');
            return d.toLocaleDateString();
            
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
