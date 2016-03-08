/**
 * Created by bluesialia on 27/02/16.
 */
'use strict';

var map;
var mapDiv;
var markers= [];

window.onload = function() {
	mapDiv = document.getElementById('map');

	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(initMap);
	} else {
		alert("Geolocation is not supported by this browser. Not every feature may work correctly")
		initMap();
	}
};

function initMap(position) {
	var latitude = (position) ? position.coords.latitude : 0;
	var longitude = (position) ? position.coords.longitude : 0;
	map = new google.maps.Map(mapDiv, {
		center: {lat: latitude, lng: longitude},
		zoom: 4
	});
}
/**
 * Places a marker in the position determined by the latitude and longitude.
 * If a message is passed the marker will display it when clicked.
 * @param message String containing HTML to display when marker is clicked
 * @param latitude Latitude of the marker
 * @param longitude Longitude of the marker
 */
function addMarker(latitude, longitude, message) {
	var marker = new google.maps.Marker({
		position: {lat: latitude, lng: longitude},
		map: map,
		animation: google.maps.Animation.DROP
	});

	if (message) {
		marker.message = new google.maps.InfoWindow({
			content: message
		});
		marker.addListener('click', function() {
			marker.message.open(map, marker);
		});
	}

	marker.setMap(map);
	markers.push(marker);
}

/**
 * Removes every marker from the map.
 */
function clearMarkers() {
	for (var i = 0; i < markers.length; i++) {
		markers[i].setMap(null);
	}
	markers = [];
}
