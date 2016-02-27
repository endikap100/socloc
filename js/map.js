/**
 * Created by bluesialia on 27/02/16.
 */
'use strict';

var mapDiv;
var map;

function initMap() {
	mapDiv = document.getElementById('map');
	map = new google.maps.Map(mapDiv, {
		center: {lat: 0, lng: 0},
		zoom: 4
	});
}