    (function(){
        google.load("visualization", "1", {packages:["table"]});
        $('#search').click(function(){
            query = find_query_params();
            query?query_data(query):error();
            
            function query_data(query) {
                $('#data-tables').empty();
                $('#data-tables').html('<h2>Searching ...</h2>');
                $.get(query)
                    .done(function(data){
                        console.log(data);
			show_data(data);
                    });

            }
            function error(){
                $('#data-tables').html('<h4 class="text-danger">WTF?? Specify at least one search category.</h4>');
                
            }
            function find_query_params() {
                var search_params = {}
                    , data_types = [];
                $('.search-item').each(function(i,item){
                    if($(item).val() !== '') {
                    search_params[$(item).prop('id')] = $(item).val();
                    }
                });
                $('.data-type').each(function(i,item){
//                $('#crime, #voter').each(function(i,item){
                    if($(item).is(':checked')) {
                        data_types.push($(item).prop('id'));
                    }
                search_params['data_types'] = data_types.join('-');
                });
                return data_types.length === 0?false:build_query(search_params);
            }
            function build_query(search_params) {
                var county = get_county();
//                console.log(county);
                var query = ['county', county]
                    ,base = '/search';
                $.each(search_params, function(key, value) {
                    query.push(key);
                    query.push(value);
                });
                return [base, query.join('|')].join('/');
                
            }
            function show_data(data){
//		console.log(data);
                $('#data-tables').empty();
                for (data_type in data.results) {
//                    console.log(data_type);
//                    console.log(data.results[data_type]);
                    if(data.results[data_type].data.length > 0) {
                        build_table(data_type, data.results[data_type]);
                    }
                }
            };
        });
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
        function build_table(data_type, data_content, page_size){
            if(data_type === 'arrests' || data_type === 'incidents' || data_type === 'accidents' || data_type === 'citations') {
                formatted_table_data = data_content.data.map(function(row) { row[0] = truncate(row[0], 15); return row; });
            }
            else { formatted_table_data = data_content.data; }
            var rows = $('.row');
            var table_width = ($(rows[0]).width() - 50) + 'px';
            page_size = page_size || 20;
            var data = new google.visualization.DataTable();
            data_content.headings.forEach( function(heading) {
                data.addColumn("string",heading);
            });
            data.addRows(formatted_table_data);
            var options = {page:"enable",pageSize:20};
            var table_div_id = 'data-table-' + data_type;
            var table_div = '<h2 style="text-transform: capitalize">' + data_type + ': ' + data_content.data.length + ' records</h2><div style="width:100%" id="' + table_div_id + '"></div>';
            $('#data-tables').append(table_div);
            var table = new google.visualization.Table(document.getElementById(table_div_id));
            table.draw(data,options);
        }
        function truncate(string,length) {
            string = string.length > length ? string.substr(0,length-1) + ' ...': string;
            return string;
        }
    })();
