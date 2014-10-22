(function(){
    google.load('visualization', '1', {packages: ['controls']});
    var breadcrumbs = {};
    var geocoder = new google.maps.Geocoder();
    var map, start_zoom = 15;
	$.getJSON('lib/data/index.js', function(data){
		var how_many = data.results.length;
		var slices = slice_data(data.results,4);
        $('#content-row').empty();
        slices.forEach(function(counties){
            var html = fill_template('column3', {'counties': counties});
            $('#content-row').append(html);
        });
        $('.counties').on('click', function(e){
            e.preventDefault();
            var county = $(this).data('county');
            fetch_facility_data(county);
        });
	});
    
    function draw_table(facility_data, place){
        $('#content-row').empty();
        
        var data = new google.visualization.DataTable();
        var options = {};
        data.addColumn("string","Name");
        data.addColumn("string","Address");
        data.addColumn("string","City");
        data.addColumn("date","Insp. Date");
        data.addColumn("number","Score");
        data.addColumn("string","Details");
        data.addRows(facility_data);
        options['page'] = 'enable';
        options['pageSize'] = 20;
        options['pagingSymbols'] = {prev: 'prev', next: 'next'};
        options['pagingButtonsConfiguration'] = 'auto';
        options['allowHtml'] = true;
//        var view_data = new google.visualization.DataView(data);
//        var view_data = new google.visualization.DataTable(data);
        var filters = [];
        var stringFilter = new google.visualization.ControlWrapper({
            'controlType': 'StringFilter',
            'containerId': 'text-filter',
            'options': {
                'matchType': 'any',
                'filterColumnLabel': 'Name',
                'ui': {
                    'label': 'Name'
                    ,'cssClass': 'text-control'
                }
            }
        
        });

        filters.push(stringFilter);
        // Define a table visualization
        var table = new google.visualization.ChartWrapper({
          'chartType': 'Table',
          'containerId': 'data-table',
          'options': options
        });
        // Create the dashboard.
        var html = fill_template('data-table',{'place': place});
        $('#content-row').html(html);
        make_breadcrumbs();
        var data_dashboard = new google.visualization.Dashboard(document.getElementById('data-dashboard'));
        var t;
        google.visualization.events.addListener(data_dashboard, 'ready', function(){
            table_clicks();
            t = table.getChart();
            google.visualization.events.addListener(t, 'sort', function(){
                table_clicks();
            });
            google.visualization.events.addListener(t, 'page', function(){
                table_clicks();
            });
        });
        
          // Configure the string filter to affect the table contents
        data_dashboard.bind(filters, table).
        // Draw the dashboard
          draw(data);
          
    }

    function table_clicks(){
        $('.show-facility').on('click', function(e){
            e.preventDefault();
            var facility_id = $(this).data('fid');
            fetch_facility_details(facility_id);
        });
            $('.show-city').on('click', function(e){
            e.preventDefault();
            var city = $(this).data('city');
            fetch_city_data(city);
        });    
    }
    function show_facility_details(facility_data) {
        facility_data['item_comments'] = format_comments(facility_data['item_comments']);
        var html = fill_template('facility-details', facility_data);
        $('#content-row').empty();
        $('#content-row').html(html);
        make_breadcrumbs();
        geocode(facility_data['addr_line1'], facility_data['addr_city']);
    }
    
    function fetch_facility_data(county){
        breadcrumbs = {};
        var url = 'lib/data/' + encodeURIComponent(slugify(county)) + '/index.js';
        $.getJSON(url, function(data){
            var facility_data = data.results.map(format_facility_data);
            draw_table(facility_data, county);
            breadcrumbs.county = county;
        });
    
    }
    function fetch_city_data(city){
        breadcrumbs.city && delete breadcrumbs.city;
        var url = 'lib/data/' + encodeURIComponent(slugify(breadcrumbs.county)) + '/' + encodeURIComponent(slugify(city)) + '.js';
        $.getJSON(url, function(data){
            var city_data = data.results.map(format_facility_data);
            draw_table(city_data, city);
            breadcrumbs.city = city;
        });
    
    }

    function fetch_facility_details(facility_id){
        var url = 'lib/data/' + encodeURIComponent(slugify(breadcrumbs.county)) + '/' + encodeURIComponent(slugify(facility_id)) + '.js';
        $.getJSON(url, function(data){
            var facility_data = data.results;
            show_facility_details(facility_data);
        });
    
    }

function slugify(str) {
    return str.toLowerCase().replace(' ', '-');

}
    function draw_map(latlon) {
        var mapOptions = {
            zoom: start_zoom,
            center: latlon,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        map = new google.maps.Map(document.getElementById("map"), mapOptions);
        var marker = new google.maps.Marker({
            position: latlon,
            map: map,
            icon: 'lib/img/pin-red.png',
            visible: true
        });    
    }
    
    function geocode(street, city, st) {
        var st = st || 'NC';
        var address = [street, city, st].join(', ');
        var latlon = false;
        geocoder.geocode( { 'address': address}, function(results, status) {
            if (status === google.maps.GeocoderStatus.OK) {
                draw_map(results[0].geometry.location);
            }
        });
        
    }
    
    function format_comments(comments){
        var comment_lines = comments.split(';').map( function (c){
            return capitalize( c.trim());
        });
        
        return comment_lines;
    }
    
    function format_facility_data(data){
    
        data[3] = {v: new Date(data[3]), f: data[3] };
        data[2] = '<a href="" class="show-city" data-city="' + data[2] + '">' + data[2] + '</a>';

        data[5] = '<a href="" class="show-facility" data-fid="' + data[5] + '">Details</a>';
        return data;
    
    }
    
    function make_breadcrumbs() {
        var bc_pieces = [];
        for (key in breadcrumbs) {
            bc_pieces.push({'param': key, 'value': breadcrumbs[key]});
        }
        var context = {'breadcrumbs': bc_pieces};
        var filled_breadcrumbs = fill_template('breadcrumbs-template', context);
        $('#breadcrumbs').html(filled_breadcrumbs);
        $('.breadcrumb-county').on('click', function(e){
            e.preventDefault();
            var county = $(this).data('county');
            fetch_facility_data(county);            
        });
        $('.breadcrumb-city').on('click', function(e){
            e.preventDefault();
            var city = $(this).data('city');
            fetch_city_data(city);            
        });
    }
    
	function slice_data(data,how_many) {
		var slices = []
          , slice_start = 0
          , slice_end = 0
          , slice_size = 0;
		//each piece has same number
		if(data.length%how_many === 0) {
			slice_size = data.length/how_many;
            for(var i = 0; i < how_many; i++){
                slice_end = i?slice_end + slice_size: slice_size;
                slices.push(data.slice(slice_start, slice_end));
                slice_start += slice_size;
            }
		}
        else{
            console.log(data.length%how_many);
        }
        return slices;
	}
    function fill_template(id,context) {
        var source = $('#' + id).html();
        var template = Handlebars.compile(source);
        return template(context);
    }
    
    function capitalize(s) {
        return s && s[0].toUpperCase() + s.slice(1);
    }
})()
