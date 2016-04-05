/**
 * Created by bluesialia on 27/02/16.
 */
'use strict';

var map;
var mapDiv;
var markers = [];
var apiUrl = 'http://socloc.cloudapp.net:9000';

window.onload = function () {
	mapDiv = document.getElementById('map');

	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(initMap);
	} else {
		alert("Geolocation is not supported by this browser. Not every feature may work correctly");
		initMap();
	}

	getTwitterLocations();
};

/**
 * Loads a Google Map inside the HTML.
 * @param {google.maps.Map} [position] Center of the map.
 */
function initMap(position) {
	var latitude = (position) ? position.coords.latitude : 0;
	var longitude = (position) ? position.coords.longitude : 0;
	map = new google.maps.Map(mapDiv, {
		center: {lat: latitude, lng: longitude},
		zoom: 4
	});
}

/**
 * Gets the location of several tweets from the API and calls addMarkers().
 */
function getTwitterLocations() {
	var xhr = new XMLHttpRequest();

	xhr.onload = function () {
		if (xhr.status == 200) {
			var json = JSON.parse(xhr.responseText);
			addMarkers(json);
		}
	};
	xhr.open("GET", apiUrl, true);
	xhr.send();
}

/**
 * Places a collection of markers from the api.
 * For each marker, if it has a message, the marker will display it when clicked.
 * @param jsonObj JSON containing the markers from the api.
 */
function addMarkers(jsonObj) {
	for (var hashtag in jsonObj) {
		if (jsonObj.hasOwnProperty(hashtag)) {
			for (var i = jsonObj[hashtag].length; i <= 0; i--) {
				addMarker(jsonObj[hashtag][i][0], jsonObj[hashtag][i][1], hashtag);
			}
		}
	}
}

/**
 * Places a marker in the position determined by the latitude and longitude.
 * If a message is passed the marker will display it when clicked.
 * @param {float} latitude Latitude of the marker.
 * @param {float} longitude Longitude of the marker.
 * @param {String} [message] HTML to display when marker is clicked.
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
		marker.addListener('click', function () {
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
