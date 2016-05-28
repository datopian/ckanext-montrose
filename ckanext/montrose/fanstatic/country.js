(function(){
	'use strict'
	$(document).ready(function(){
	
		var base_url = ckan.sandbox().client.endpoint;
		$('#montrose_map').on('change', function(){
			// Get resource id
			var resource_id = $('#montrose_map option:selected').val();
			
			// Build API url to fetch map properties
			var url = base_url + '/api/action/' + 'montrose_resource_show_map_properties?id=' + resource_id;
			
			
			// Fetch map properties
			$.getJSON(url, function( data ) {
			  var options = $("#montrose_map_main_property");
			  $.each( data.result, function(idx, elem){
			    options.append(new Option(elem.text, elem.value));
			  });
			});
			
			// Show drop down
			$('.montrose_map_main_property').removeClass('hidden');
			
		});
	});
})($);