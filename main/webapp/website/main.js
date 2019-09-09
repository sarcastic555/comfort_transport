var map;
var load_location_id = null;
var bus_data_file = new XMLHttpRequest();
var buses0;
var buses1;
var buses_mid;
var num_colors = 8;

var load_interval = 30000;
var insert_locations_interval = 500;
var last_update_time;

function initialize() { 
    var latlng = new google.maps.LatLng(35.680865,139.767036);
    var opts = {
        zoom: 14,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    
    var useragent = navigator.userAgent;
    var mapdiv = document.getElementById("map_canvas");
    if (useragent.indexOf('iPhone') != -1 || useragent.indexOf('Android') != -1){
        mapdiv.style.width = '100%';
        mapdiv.style.height = '100%';
    }
    map = new google.maps.Map(mapdiv, opts);
};


function Bus(lat, lng, date, number, route_number){
    this.lat = lat;
    this.lng = lng;
    this.date = date;
    this.number = number;
    this.route_number = route_number;
    var m_latlng = new google.maps.LatLng(lat, lng);
    hash_key = route_number % num_colors;
    var img_url = './bus_img/' + hash_key.toString(10) + '.png';
    var image = {
        url : img_url,
        scaledSize : new google.maps.Size(48, 48)
    };
    this.marker = new google.maps.Marker({
        position: m_latlng,
        icon:image
    });
};

function buses_copy_1_to_mid(){//内挿バスデータにコピー
    if(!buses_mid){//最初のロード時はコピー
        buses_mid = buses_copy(buses1);
        return;
    }
    
    var num_mid_buses = buses_mid.length;
    var flag_array = Array(num_mid_buses);
    for(var j=0; j<num_mid_buses; j++){
        flag_array[j] = false;
    }
    
    for(var i=0; i<buses1.length; i++){
        var flag = false;
        for(var j=0; j<num_mid_buses; j++){
            if(buses1[i].number == buses_mid[j].number){
		flag = true;
		flag_array[j] = true;
		break;
            }
        }
        if(flag == false){//新しいバスがあったとき
            buses_mid.push(new Bus(buses1[i].lat, buses1[i].lng, buses1[i].date, buses1[i].number, buses1[i].route_number));
            buses_mid[buses_mid.length-1].marker.setMap(map);
        }
    }
    for(var j=0; j<num_mid_buses; j++){
        if(flag_array[j] == false){//バスが消えたとき
            buses_mid[j].marker.setVisible(false);
        }
    }
}

function buses_copy(buses_src){//バス情報コピー
    if(!buses_src){
        return null;
    }
    num_buses = buses_src.length;
    var buses_dst = Array(num_buses);
    for(var i=0; i<num_buses; i++){
        src = buses_src[i];
        buses_dst[i] = new Bus(src.lat, src.lng, src.date, src.number, src.route_number);
    }
    return buses_dst;
}

function bus_move(bus, lat, lng){//バスを動かす
    bus.lat = lat;
    bus.lng = lng;
    bus.marker.setPosition(new google.maps.LatLng(lat, lng));
}

function pin_bus_markers(buses){//バスアイコン表示
    if(!buses){
        return;
    }
    for(var i=0; i<buses.length; i++){    
        buses[i].marker.setMap(map);
    }
};

function insert_locations(){//バス位置内挿
    if(!buses0){
        return;
    }
    var now = new Date();
    var now_milliSec = 1000 * now.getSeconds() + now.getMilliseconds();
    var last_milliSec = 1000 * last_update_time.getSeconds() + last_update_time.getMilliseconds();
    var passed_milliSec = (60 * 1000 + now_milliSec - last_milliSec) % (60 * 1000);
    var alpha = passed_milliSec / load_interval;
    for(var i=0; i<buses1.length; i++){
        for(var j=0; j<buses0.length; j++){
            if(buses0[j].number == buses1[i].number){
		var lat = alpha * buses1[i].lat + (1.0 - alpha) * buses0[j].lat;
		var lng = alpha * buses1[i].lng + (1.0 - alpha) * buses0[j].lng;
		for(var k=0; k<buses_mid.length; k++){
                    if(buses1[i].number == buses_mid[k].number){
			bus_move(buses_mid[k], lat, lng);
			break;
                    }
		}
		break;
            }
        }
    }
}

function extract_busroute_number (str_busroute){
    var busroute_num = 0;
    var loop_num = 1;
    while(loop_num<str_busroute.length){
        var num_tmp = str_busroute.length - loop_num;
        if( !isNaN(str_busroute[num_tmp]) ){
            loop_num++;
            continue;
        }else if (str_busroute[num_tmp] === "-" ){
            loop_num++;
            continue;
        }else{
            break;
        }
    }
    
    if(loop_num === 1){
        busroute_num = 0;
    }else{
        busroute_num = str_busroute.slice(1-loop_num);
        busroute_num = busroute_num.replace(/-/g, "");
    }
    return Number(busroute_num);
}

bus_data_file.onload = function () {//バス情報ロード      
        var text = bus_data_file.responseText
    var bus_data = JSON.parse(text);
    buses0 = buses_copy(buses1);
    buses1 = Array(bus_data.length);
    for(var i=0; i<buses1.length; i++){
        var lat = bus_data[i]["geo:lat"];
        var lng = bus_data[i]["geo:long"];
        var date = bus_data[i]["dc:date"];
        var number = Number(bus_data[i]["odpt:busNumber"]);
        var route_number = extract_busroute_number(bus_data[i]["odpt:busroute"])
        buses1[i] = new Bus(lat, lng, date, number, route_number);
    }
    
    buses_copy_1_to_mid();
    last_update_time = new Date();
    insert_locations()
    pin_bus_markers(buses_mid);
};

function hex(s) {
    console.log("function hex(s)")
    console.log(s)
    var result="";
    for(var i=0;i<s.length;++i){
        var h = ("0"+s.charCodeAt(i).toString(16)).substr(-2);
        result += h;
    }
    return result;
};

function PlotBusStop(url, icon_file){
    console.log(url);
    　　　　var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4) {
            if (xmlhttp.status == 200) {
		var data = JSON.parse(xmlhttp.responseText);
		//console.log(data.length);
		for (step = 0;step<data.length;step++) {
                    //console.log(data[step].lat);
                    //console.log(data[step].lon);
                    var m_latlng = new google.maps.LatLng(data[step].lat,data[step].lon);
                    //console.log(hex(data[step].busroutePattern)%8);
                    //marker_url = getMarker(hex(data[step].busroutePattern)%8);
                    //marker_url = getMarker(hex("aho")%8);
                    marker_url = "http://unno.jpn.org/gmap/icons/blue-dot.png"
                    //console.log("print color");
                    //console.log(marker_url);
                    marker = new google.maps.Marker({
			position: m_latlng,
			title: url,
			icon: {
			    url: marker_url
			}
                    });
                    marker.setMap(map);
		}
            }
        }
    }
    xmlhttp.open("GET",url);
    xmlhttp.send();
};

function getMarker(id){
    marker_file="red-dot.png"
    if (id==0){
        marker_file="red-dot.png"
    } else if (id==1){
        marker_file="blue-dot.png"
    } else if (id==2){
        marker_file="green-dot.png"
    } else if (id==3){
        marker_file="ltblue-dot.png"
    } else if (id==4){
        marker_file="yellow-dot.png"
    } else if (id==5){
        marker_file="purple-dot.png"
    } else if (id==6){
        marker_file="pink-dot.png"
    } else if (id==7){
        marker_file="orange-dot.png"
    }
    return "http://unno.jpn.org/gmap/icons/"+marker_file
};

function load_location(){
    bus_data_file.open("GET", "https://api-tokyochallenge.odpt.org/api/v4/odpt:Bus?odpt:operator=odpt.Operator:SeibuBus&acl:consumerKey=2deef49e96744c2566cca5bb289318cd28490a662d82b8e62a071d32afe3fc3c");
    //bus_data_file.open("GET", "https://api-tokyochallenge.odpt.org/api/v4/odpt:Bus?odpt:operator=odpt.Operator:Toei&acl:consumerKey=2deef49e96744c2566cca5bb289318cd28490a662d82b8e62a071d32afe3fc3c");
    bus_data_file.send();
};

function update_time(){
    var now = new Date();
    var sec = (60 + now.getSeconds() - last_update_time.getSeconds()) % 60;
    var text = "最終更新から"+ sec +"秒";
    target = document.getElementById('time');
    target.innerHTML = text;
};

function toCurrent() {
    console.log("abs")
    console.log(hex("abc"))
    console.log(hex("abc")%9)
    
    // 30秒ごとにバス位置座標データを読み込む
    load_location();
    load_location_id = setInterval("load_location()", load_interval);
    
    // 1秒ごとに最終更新時間の表示を更新
    update_time_id = setInterval("update_time()", 1000);
    // 0.5秒ごとにバスの位置を内挿
    insert_locations_id = setInterval("insert_locations()", insert_locations_interval);
    
    // バス停座標を地図上にマーカー表示
    let bus_company_list = ["Toei", "KantoBus", "SeibuBus", "KokusaiKogyoBus", "NishiTokyoBus", "TokyuBus"];
    for(let i = 0; i < bus_company_list.length; i++) {
        PlotBusStop("busstop_data/coord_busstops_"+bus_company_list[i]+".json", "blue-dot.png")
    }
    
    // バスロケーション情報の蓄積jsonを読み込む
    var ReadBusLocationAccumulation = function(file_path){
        var bus_latlon_list = [] // 緯度経度
        var bus_info_list = [] // バス路線ID
        console.log(file_path);
	var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function () {
            if (xmlhttp.readyState == 4) {
		if (xmlhttp.status == 200) {
                    var data = JSON.parse(xmlhttp.responseText);
                    for (step = 0;step<data.length;step++) {
			bus_latlon_list.push({lat: Number(data[step].lat), lng: Number(data[step].long)})
			bus_info_list.push({busroute: data[step].busroute, busroute_index: data[step].busroute_index})
                    }
		}
            }
        }
        xmlhttp.open("GET", file_path, false); // 第3引数にfalseを与えると同期処理となるので完了を待つ
        xmlhttp.send();
        return {location_list:bus_latlon_list, info_list:bus_info_list};
    };
    
    var read_bus_location_result1 = ReadBusLocationAccumulation("buslocation_data/bus_location_all.json");
    console.log("output length")
    console.log(read_bus_location_result1.location_list.length)
    console.log(read_bus_location_result1.info_list.length)
    console.log(read_bus_location_result1.location_list[0])
    console.log(read_bus_location_result1.info_list[0].busroute_index)
    
    var bus_routepattern_index_stored = read_bus_location_result1.info_list[0].busroute_index // 最初のデータのバスルートインデックスで初期化
    var route_location_list = []
    for(let i = 0; i < read_bus_location_result1.location_list.length; i++) {
        if (read_bus_location_result1.info_list[i].busroute_index==bus_routepattern_index_stored && i < read_bus_location_result1.location_list.length-1){
            console.log(i)
            console.log("push")
            route_location_list.push(read_bus_location_result1.location_list[i])
        } else {
            console.log(i)
            console.log("plot")
            // バスルート表示
            var flightPath1 = new google.maps.Polyline({
		path: route_location_list,
		geodesic: true,
		strokeColor: '#FF0000',
		strokeOpacity: 1.0,
		strokeWeight: 2
            });
            flightPath1.setMap(map);
            bus_routepattern_index_stored += 1
            route_location_list = []
        }
    }
    
    
    function success(position) {
        map.panTo(new google.maps.LatLng(position.coords.latitude,position.coords.longitude));
        map.panTo(new google.maps.LatLng(35.699059, 139.416267))
    };
    function error(err){
        switch(err.code) {
        case 1: // PERMISSION_DENIED
            window.alert("位置情報の利用が許可されていません");
                break;
        case 2: // POSITION_UNAVAILABLE
            window.alert("現在位置が取得できませんでした");
                break;
        case 3: // TIMEOUT
            window.alert("タイムアウトになりました");
            break;
        default:
            window.alert("その他のエラー(エラーコード:"+error.code+")");
                break;
        }
        output.innerHTML = "座標位置を取得できません";
    };
    var output = document.getElementById("result");
    if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(success, error);
    }   
    if (!navigator.geolocation){//Geolocation apiがサポートされていない場合
        output.innerHTML = "<p>Geolocationはあなたのブラウザーでサポートされておりません</p>";
        return;
    }
    
};

