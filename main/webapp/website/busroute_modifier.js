var map;
var load_location_id = null;
var bus_data_file = new XMLHttpRequest();
var buses0;
var buses1;
var buses_mid;
var num_colors = 7;
var stops;
var load_interval = 30000;
var insert_locations_interval = 500;
var last_update_time;
var bus_icon_size;
var bus_stop_icon_size
function initialize() { 
    var latlng = new google.maps.LatLng(35.680865,139.767036);
    var opts = {
        zoom: 11,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
	draggable: true // マーカーをdraggableにするためには地図をundraggableにする必要あると思ったがそうではない？！
    };
    
    var useragent = navigator.userAgent;
    var mapdiv = document.getElementById("map_canvas");
    if (useragent.indexOf('iPhone') != -1 || useragent.indexOf('Android') != -1){
        mapdiv.style.width = '97%';
        mapdiv.style.height = '93%'; // スマートフォンの場合は多少上下左右にマージンを残しておく
	bus_icon_size = 80; // スマートフォンは画面が小さいのでバスアイコンサイズを大きくする
	bus_stop_icon_size = 85; // スマートフォンは画面が小さいのでバスアイコンサイズを大きくする
    } else {
	bus_icon_size = 48; // for PC
	bus_stop_icon_size = 48; // for PC
    }
    map = new google.maps.Map(mapdiv, opts);

    toCurrent(); //現在地にジャンプしてバス停やバス位置を表示するのはデフォルトとする(クリックを要求しない)
};

function GetBusMarkerImgFromRouteNum(route_number){
    hash_key = route_number % num_colors;
    img_file = './bus_img/' + hash_key.toString(10) + '.png';
    return img_file
};
function GetColorStringFromRouteNum(route_number){
    hash_key = route_number % num_colors;
    if (hash_key==0){
	return "black";
    } else if (hash_key==1){
	return "red";
    } else if (hash_key==2){
	return "#02F702"; //lightgreen (see https://lab.syncer.jp/Web/API/Google_Maps/JavaScript/Rectangle/strokeColor/)
    } else if (hash_key==3){
	return "blue";
    } else if (hash_key==4){
	return "yellow";
    } else if (hash_key==5){
	return "cyan";
    } else if (hash_key==6){
	return "magenta";
    } else {
	return "black";
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
function toCurrent() {
    console.log("abs")
    
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
    var busroute = "";
    var plot_color = ""
    var plot_route_index = 133; //このルートインデックスのルートのみ地図上に表示

    for(let i = 0; i < read_bus_location_result1.location_list.length; i++) {
	if (read_bus_location_result1.info_list[i].busroute_index==plot_route_index+1 || i == read_bus_location_result1.location_list.length-1){
	    var flightPath1 = new google.maps.Polyline({
		path: route_location_list,
		geodesic: true,
		strokeColor: GetColorStringFromRouteNum(extract_busroute_number(busroute)),
		strokeOpacity: 1.0,
		strokeWeight: 2
	    });
	    flightPath1.setMap(map);
	    
	    //マーカーも表示する
	    for (let j = 0; j<route_location_list.length; j++){
		var marker = new google.maps.Marker({
		    position: route_location_list[j],
		    icon: {
			url: "icon_img/flag.png",
			scaledSize: new google.maps.Size(40, 40)
		    },
		    draggable: true
                });
                marker.setMap(map);
		
		infoWindow = new google.maps.InfoWindow({ // 吹き出しの追加
		    content: String(j)
		});
		infoWindow.open(map, marker);

		google.maps.event.addListener( marker, 'dragend', function(ev){
		    console.log("dragend")
		    // イベントの引数evの、プロパティ.latLngが緯度経度。
		    document.getElementById('latlon').value = String(ev.latLng.lat())+","+String(ev.latLng.lng());
		});

	    }
	    break;
	}
        if (read_bus_location_result1.info_list[i].busroute_index==plot_route_index){
            route_location_list.push(read_bus_location_result1.location_list[i]);
	    busroute = read_bus_location_result1.info_list[i].busroute
        }
    }
    
    map.panTo(new google.maps.LatLng(35.742985, 139.538275)) // ひばりヶ丘らへんにPanToする
    
};

