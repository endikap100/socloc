/**
 * Created by bluesialia on 27/02/16.
 */
'use strict';
var apiUrl = 'http://socloc.cloudapp.net:9000';

var map;
var mapDiv;
var markers = [];

var hashtag_listDiv;
var hashtag_list = {};

window.onload = function () {
	mapDiv = document.getElementById('map');
	hashtag_listDiv = document.getElementById('hashtag_list');

	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(initMap);
	} else {
		alert("Geolocation is not supported by this browser. Not every feature may work correctly");
		initMap();
	}
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
	google.maps.event.addListenerOnce(map, 'google-map-ready', getTwitterLocations());
}

/**
 * Gets the location of several tweets from the API and calls loadApiCall().
 */
function getTwitterLocations() {
	var xhr = new XMLHttpRequest();

	xhr.onload = function () {
		if (xhr.status == 200) {
			var json = JSON.parse(xhr.responseText);
			loadApiCall(json);
		}
	};
	xhr.open("GET", apiUrl, true);
	xhr.send();
}

/**
 * Loads a collection of markers from the api.
 * @param jsonObj JSON containing the markers from the api.
 */
function loadApiCall(jsonObj) {
	for (var hashtag in jsonObj) {
		if (jsonObj.hasOwnProperty(hashtag)) {
			var currentHashtagList = [];
			for (var i = jsonObj[hashtag].length - 1; i >= 0; i--) {
				var split = jsonObj[hashtag][i].split(',');
				var longitude = parseFloat(split[0]);
				var latitude = parseFloat(split[1]);

				var marker = new google.maps.Marker({
					position: {lat: latitude, lng: longitude},
					animation: google.maps.Animation.DROP
				});

				currentHashtagList.push(marker);
			}

			hashtag_list[hashtag] = currentHashtagList;

			addHashtag(hashtag);
		}
	}
}

/**
 * Places a list of markers.
 * For each marker, if it has a message, the marker will display it when clicked.
 * @param markerList List containing the markers from the api.
 * @param {String} [message] HTML to display when a marker is clicked.
 */
function addMarkers(markerList, message) {
	for (var i = markerList.length - 1; i >= 0; i--) {
		addMarker(markerList[i], message);
	}
}

/**
 * Places a marker in the position determined by the latitude and longitude.
 * If a message is passed the marker will display it when clicked.
 * @param {Number} latitude Latitude of the marker.
 * @param {Number} longitude Longitude of the marker.
 * @param {String} [message] HTML to display when marker is clicked.
 */
function addMarkerWithParameters(latitude, longitude, message) {
	var marker = new google.maps.Marker({
		position: {lat: latitude, lng: longitude},
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
 * Places a marker.
 * If a message is passed the marker will display it when clicked.
 * @param marker Marker to place in the map.
 * @param {String} [message] HTML to display when marker is clicked.
 */
function addMarker(marker, message) {
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

function addHashtag(hashtag) {
	var li = document.createElement('li');
	var a = document.createElement('a');
	a.href = 'javascript:;';
	a.className = 'link';
	a.innerHTML = hashtag;

	a.onclick = function() {
		clearMarkers();
		addMarkers(hashtag_list[hashtag], hashtag);
	};

	li.appendChild(a);
	hashtag_listDiv.appendChild(li);
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
