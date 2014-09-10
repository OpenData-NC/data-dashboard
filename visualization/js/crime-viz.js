(function(){
    var counties = [
        'Cabarrus',
        'Orange',
        'Wake',
        'Franklin',
        'Wilson',
        'Rowan',
        'Lee',
        'Catawba',
        'Buncombe',
        'Caldwell',
        'Forsyth',
        'Edgecombe',
        'Cumberland',
        'New Hanover',
        'Burke',
        'Davidson',
        'Lincoln',
        'Union',
        'Cleveland',
        'Guilford'
    ];

    var group_by_types = [
        'sex',
        'race',
        'category'
    ];
    var county_centers = {
      Alamance: [ 36.0334701538086, -79.3997421264648 ],
      Alexander: [ 35.9334716796875, -81.1831359863281 ],
      Alleghany: [ 36.483455657959, -81.1164703369141 ],
      Anson: [ 34.9834861755371, -80.0997772216797 ],
      Ashe: [ 36.4334564208984, -81.4998245239258 ],
      Avery: [ 36.1001243591309, -81.9331665039062 ],
      Beaufort: [ 35.4334983825684, -76.866325378418 ],
      Bertie: [ 36.0668144226074, -76.9663391113281 ],
      Bladen: [ 34.6334991455078, -78.5663986206055 ],
      Brunswick: [ 34.066837310791, -78.2663879394531 ],
      Buncombe: [ 35.6001091003418, -82.5165100097656 ],
      Burke: [ 35.7667961120605, -81.6998138427734 ],
      Cabarrus: [ 35.3668098449707, -80.5664596557617 ],
      Caldwell: [ 35.9501266479492, -81.5498199462891 ],
      Camden: [ 36.3668174743652, -76.182991027832 ],
      Carteret: [ 34.8001556396484, -76.6996536254883 ],
      Caswell: [ 36.4001388549805, -79.349739074707 ],
      Catawba: [ 35.6667976379395, -81.2331390380859 ],
      Chatham: [ 35.700138092041, -79.2664031982422 ],
      Cherokee: [ 35.1500778198242, -84.0332412719727 ],
      Chowan: [ 36.1501579284668, -76.6496658325195 ],
      Clay: [ 35.0500869750977, -83.7665557861328 ],
      Cleveland: [ 35.3334579467773, -81.5498123168945 ],
      Columbus: [ 34.2504501342773, -78.6330718994141 ],
      Craven: [ 35.133487701416, -77.0663375854492 ],
      Cumberland: [ 35.0501594543457, -78.8664093017578 ],
      Currituck: [ 36.3126564025879, -75.937141418457 ],
      Dare: [ 35.7504501342773, -75.7662887573242 ],
      Davidson: [ 35.8167991638184, -80.2331085205078 ],
      Davie: [ 35.9334716796875, -80.5331039428711 ],
      Duplin: [ 34.9501686096191, -77.94970703125 ],
      Durham: [ 36.0334777832031, -78.8663940429688 ],
      Edgecombe: [ 35.9001579284668, -77.5830307006836 ],
      Forsyth: [ 36.1334686279297, -80.2330932617188 ],
      Franklin: [ 36.0668144226074, -78.3330535888672 ],
      Gaston: [ 35.3001365661621, -81.1997985839844 ],
      Gates: [ 36.4334869384766, -76.6996765136719 ],
      Graham: [ 35.3500862121582, -83.7998962402344 ],
      Granville: [ 36.3168106079102, -78.6497192382812 ],
      Greene: [ 35.5007171630859, -77.6663589477539 ],
      Guilford: [ 36.0667991638184, -79.7997512817383 ],
      Halifax: [ 36.2501487731934, -77.6496963500977 ],
      Harnett: [ 35.383487701416, -78.849739074707 ],
      Haywood: [ 35.5500984191895, -82.9665298461914 ],
      Henderson: [ 35.3501205444336, -82.4665069580078 ],
      Hertford: [ 36.3501472473145, -76.9830169677734 ],
      Hoke: [ 35.0168304443359, -79.2664184570312 ],
      Hyde: [ 35.5001678466797, -76.2663040161133 ],
      Iredell: [ 35.7834663391113, -80.8831253051758 ],
      Jackson: [ 35.2667694091797, -83.1331939697266 ],
      Johnston: [ 35.5334854125977, -78.3997192382812 ],
      Jones: [ 35.0168304443359, -77.3996810913086 ],
      Lee: [ 35.4668159484863, -79.1830749511719 ],
      Lenoir: [ 35.2334976196289, -77.6496887207031 ],
      Lincoln: [ 35.483470916748, -81.2498016357422 ],
      Macon: [ 35.150089263916, -83.4498825073242 ],
      Madison: [ 35.8667678833008, -82.6665267944336 ],
      Martin: [ 35.8334884643555, -77.1496810913086 ],
      McDowell: [ 35.7001152038574, -82.0498275756836 ],
      Mecklenburg: [ 35.2668075561523, -80.8497924804688 ],
      Mitchell: [ 36.016788482666, -82.1331787109375 ],
      Montgomery: [ 35.3501358032227, -79.8997650146484 ],
      Moore: [ 35.3001480102539, -79.4830780029297 ],
      Nash: [ 35.9668159484863, -77.9663696289062 ],
      'New Hanover': [ 34.2504501342773, -77.8663711547852 ],
      Northampton: [ 36.4168167114258, -77.3663558959961 ],
      Onslow: [ 34.7504386901855, -77.4330139160156 ],
      Orange: [ 36.0668067932129, -79.1164016723633 ],
      Pamlico: [ 35.1334991455078, -76.7496490478516 ],
      Pasquotank: [ 36.3001556396484, -76.2829895019531 ],
      Pender: [ 34.5004386901855, -77.9663772583008 ],
      Perquimans: [ 36.2168197631836, -76.4496536254883 ],
      Person: [ 36.3834648132324, -78.9663925170898 ],
      Pitt: [ 35.5834846496582, -77.3830184936523 ],
      Polk: [ 35.283447265625, -82.1664962768555 ],
      Randolph: [ 35.700138092041, -79.8164215087891 ],
      Richmond: [ 35.0029258728027, -79.7525482177734 ],
      Robeson: [ 34.6334991455078, -79.0997619628906 ],
      Rockingham: [ 36.4001388549805, -79.783088684082 ],
      Rowan: [ 35.6501388549805, -80.5164489746094 ],
      Rutherford: [ 35.4001197814941, -81.9164886474609 ],
      Sampson: [ 34.9668388366699, -78.3997192382812 ],
      Scotland: [ 34.8334884643555, -79.4997711181641 ],
      Stanly: [ 35.3334808349609, -80.2497787475586 ],
      Stokes: [ 36.4001388549805, -80.2497634887695 ],
      Surry: [ 36.4001274108887, -80.6831207275391 ],
      Swain: [ 35.4667587280273, -83.4832153320312 ],
      Transylvania: [ 35.2167778015137, -82.7831802368164 ],
      Tyrrell: [ 35.8168258666992, -76.21630859375 ],
      Union: [ 35.0001487731934, -80.5497894287109 ],
      Vance: [ 36.3668098449707, -78.3997192382812 ],
      Wake: [ 35.7834739685059, -78.633056640625 ],
      Warren: [ 36.3834800720215, -78.0997085571289 ],
      Washington: [ 35.83349609375, -76.5996627807617 ],
      Watauga: [ 36.2334594726562, -81.6998291015625 ],
      Wayne: [ 35.3668251037598, -77.9999923706055 ],
      Wilkes: [ 36.216796875, -80.9997940063477 ],
      Wilson: [ 35.7168197631836, -77.9163665771484 ],
      Yadkin: [ 36.1501388549805, -80.6664505004883 ],
      Yancey: [ 35.9001083374023, -82.2998504638672 ] 
    };
    var major_categories = {
        'All other crimes':  'All other crimes',
        'Breaking & Entering': 'Property crimes'
        'Alcohol-related': 'All other crimes',
        'Sex crimes': 'Violent crimes',
        'Weapon-related': 'All other crimes',
        'Drug crimes': 'All other crimes',
        'Crimes against children': 'All other crimes',
        'Traffic-related': 'All other crimes',
        'Assault': 'Violent crimes',
        'Domestic violence-related': 'Violent crimes',
        'Theft': 'Property crimes',
        'Robbery': 'Violent crimes',
        'DUI': 'All other crimes',
        'Kidnapping': 'Violent crimes',
        'Auto theft-related': 'Property crimes',
        'Financial crimes': 'Property crimes',
        'Arson': 'Property crimes',
        'Homicide': 'Violent crimes',
        'Vandalism': 'Property crimes',
        'Domestic violence': 'Violent crimes'
    };

    var major_category_pins = {
        'Violent crimes': 'lib/img/pin-red.png',
        'Property crimes': 'lib/img/pin-purple.png',
        'All other crimes': 'lib/img/pin-yellow.png'
    };

    var map_styles = [
        {
          featureType: "all",
          elementType: "all",
          stylers: [
            { saturation: -100 }
          ]
        }
    ];

    var chart, table, map;
    var start_params = '/api/incidents/county/Wake/group_by/category/geo'
    function Consolidate(data, min){
        this.data = data;
        this.keys = Object.keys(data);
        this.generic_category = 'All other crimes';
        this.min = min || 10;
    }
    Consolidate.prototype.group = function() {
        var new_data = {};
        var that = this;
        var new_keys = [];
        that.keys.forEach(function(key){
            if(that.data[key] <= that.min && key !== that.generic_category) {
                that.data[that.generic_category] += that.data[key];
            }
            else {
                new_keys.push(key);
                new_data[key] = that.data[key];
            }
        });
        new_data[that.generic_category] = that.data[that.generic_category];
        new_keys.push(that.generic_category);
        that.keys = new_keys;
    };

    function GChart() {
        this.chart = new google.visualization.ColumnChart(document.getElementById("ncod-graph"));
    }
    GChart.prototype.newData = function(chart_data) {
        this.group_type = Object.keys(chart_data.grouped)[0];
        this.consolidate = new Consolidate(chart_data.grouped[this.group_type]);
        this.consolidate.group();    
        this.data = new google.visualization.DataTable();
    };
    GChart.prototype.draw = function() {
        var rows = [];
        var that = this;
        that.data.addColumn("string", "Crime Category");
        that.data.addColumn("number", "Number");
        that.consolidate.keys.forEach( function( key ){
            rows.push([key,that.consolidate.data[key]]);
        });
        that.data.addRows(rows);
        that.options = {
          hAxis:{title:"Crimes"}
          , colors: ['#56A0D3','#ADCD9E','#8E7098','#F3D469','#E1755F','#7EBEE4']
          , legend: { position: "none" }
          , animation:{
              duration: 1000,
              easing: 'out'
            }
        };
        that.chart.draw(this.data,this.options);
    };
    
    function GTable() {
        this.table = new google.visualization.Table(document.getElementById("ncod-table"));
        this.formatter = new google.visualization.DateFormat({pattern: 'M/d/yyyy'});
    }
    GTable.prototype.newData = function(table_data) {
        this.data_type = table_data.data_type;
        this.columns = table_data.headers;
        this.table_data = table_data.records;
        this.data = new google.visualization.DataTable();
    };
    GTable.prototype.draw = function() {
        var rows = [], key, date_indexes = [];
        var that = this;
        var formatted_table_data = [];
        var pdf_index;
        that.columns.forEach(function(column, index){
            key = Object.keys(column)[0];
            if(column[key] === 'datetime') {
                date_indexes.push(index);
            }
            if(key === 'pdf') {
                pdf_index = index;
            }
            that.data.addColumn(column[key], key);
        });
        that.table_data.forEach(function(row){
            date_indexes.forEach(function(i){
                row[i] = new Date(row[i]);
            });
            if(row[pdf_index]){
                if(row[pdf_index] !== ''){
                    row[pdf_index] = '<a href="' + row[pdf_index] + '" target="_blank">PDF</a>';
                }
            }
            else {
                row[pdf_index] = 'N/A';
            }
            formatted_table_data.push(row);
        });
        that.data.addRows(formatted_table_data);
        that.options = {page:"enable",pageSize:20, allowHtml: true};
        date_indexes.forEach(function(i){
            that.formatter.format(that.data,i);
        });
        that.table.draw(that.data,this.options);
    };
    function redraw(crime_data) {
        chart = new GChart();
        chart.newData(crime_data);
        chart.draw();
        table = new GTable();
        table.newData(crime_data);
        table.draw();
    }
    function fetch_data(params){
        $.getJSON(params, function(data){
            redraw(crime_data);
        });    
    }
    function make_params(pieces, group_by_geo){
        pieces.unshift('api');
        if(group_by_geo['group_by']) {
            pieces = pieces.concat(['group_by', group_by_geo['group_by']]);
        }
        if(group_by_geo['geo']) {
            pieces.push('geo');
        }
        return pieces.join('/');
    }
    google.setOnLoadCallback( function() {
        fetch_data(start_params);
        //add all change listeners here
        $('.changeme').click(function(e){
            e.preventDefault();
            chart.newData(chart_data2);
            chart.draw();
        });
    });
})();
