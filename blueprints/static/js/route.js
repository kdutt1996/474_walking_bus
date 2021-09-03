let map, infdoWindow;
let startFlag = 0, desFlag =0;
let startMarker;
let endMarker;

function initMap() {
    //init settings 
    let setting = {
      center: {lat: -34.397, lng: 150.644},
      zoom: 8
    }
    map = new google.maps.Map(document.getElementById('map'), setting);
  
    infoWindow = new google.maps.InfoWindow;
    // Try HTML5 geolocation.
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
        var pos = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };
  
        infoWindow.setPosition(pos);
        infoWindow.setContent('Location found.');
        infoWindow.open(map);
        map.setCenter(pos);
      }, function() {
        handleLocationError(true, infoWindow, map.getCenter());
      });
    } else {
      // Browser doesn't support Geolocation
      handleLocationError(false, infoWindow, map.getCenter());
    }
  
    map.addListener('click', function(e) {
        if(startFlag === 1 || desFlag === 1){
            // coords = [parseFloat(e.latLng.lat()), parseFloat(e.latLng.lng())]
            updateMarker(e.latLng, map);
        }
    });
}

let startButton = document.getElementById('startbut')
let endButton = document.getElementById('endbut')
startButton.addEventListener('click', function(){
    activateFlag(0);
});
endButton.addEventListener('click', function(){
    activateFlag(1);
});

//set start marker
function activateFlag(mode){
    if(mode == 0){
        desFlag = 0;
        startFlag = 1;
    }
    else if(mode == 1){
        desFlag = 1;
        startFlag = 0;
    }
}
  
function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
                        'Error: The Geolocation service failed.' :
                        'Error: Your browser doesn\'t support geolocation.');
    infoWindow.open(map);
}

//update marker location 
function updateMarker(coords, map){
    if(startFlag === 1){
        if(typeof startMarker !== 'undefined'){
            moveMarker(startMarker, coords);
        }
        else{
            startMarker = placeMarker(coords, map);
        }
        document.getElementById('sLat').value = coords.lat()
        document.getElementById('sLng').value = coords.lng()
    }
    else if(desFlag === 1){
        if(typeof endMarker !== 'undefined'){
            moveMarker(endMarker, coords);
        }
        else{
            endMarker = placeMarker(coords, map);
        }
        document.getElementById('dLat').value = coords.lat()
        document.getElementById('dLng').value = coords.lng()
    }
}
  
//add marker to map
function placeMarker(coords, map){
    let marker = new google.maps.Marker({
      position: coords,
      map: map
    });
    map.panTo(coords);
    return marker;
}

//move marker to new position
function moveMarker(marker, coords){
    marker.setPosition(new google.maps.LatLng(coords.lat(), coords.lng()));
    map.panTo(new google.maps.LatLng(coords.lat(), coords.lng()))
    return marker;
}