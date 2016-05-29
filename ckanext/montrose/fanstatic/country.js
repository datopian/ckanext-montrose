(function(){
	'use strict';
	var api = {
		get: function(action, params, api_ver=3){
					var base_url = ckan.sandbox().client.endpoint;
					params = $.param(params);
					var url = base_url + '/api/' + api_ver + '/action/' + action + '?' + params;
					return $.getJSON(url);
		},
		post: function(action, data, api_ver=3){
					var base_url = ckan.sandbox().client.endpoint;
					var url = base_url + '/api/' + api_ver + '/action/' + action;
					console.log(url);
					return $.post(url, JSON.stringify(data), "json");
		}
	};

	$(document).ready(function(){
		var url = window.location.pathname;
		var name = url.substr(url.lastIndexOf('/') + 1);

		// Fetch and populate datasets dropdowns

		api.get('montrose_show_datasets', {id: name}).done(function(data){
			var inputs = $('[id*=chart_dataset_]');
			  $.each( data.result, function(idx, elem) {
			    inputs.append(new Option(elem.title, elem.name));
			});

			// Dataset event handlers
			var dataset_name;
			inputs.on('change', function(){
			  	var elem = $(this);
			  	dataset_name = elem.find(":selected").val();
			  	var dataset_select_id = elem.attr('id');
			  	var resource_select_id = dataset_select_id.replace('dataset', 'resource');
			  	var resourceview_select_id = resource_select_id.replace('resource', 'resource_view');
			  	console.log(resourceview_select_id);

			  	// Empty all child selects
			  	if ($('#'+resource_select_id+' option').length > 0)
			  		$('#'+resource_select_id).find('option').not(':first').remove();

			  	console.log('#' + resourceview_select_id + '_preview');
			  	$('#' + resourceview_select_id + '_preview').empty();

			  	// Fetch and populate resources drop down
			  	api.get('montrose_dataset_show_resources', {id: dataset_name}).done(
			  		function(data){
			  			
			  			  var opts = $('#'+resource_select_id);
						  $.each( data.result, function(idx, elem) {
						    opts.append(new Option(elem.name, elem.id));
						  });

						  $('.'+resource_select_id).removeClass('hidden');
				});
			});

			// Resource event handlers

			var resource_id;
			var resource_inputs = $('[id*=chart_resource_]');
			resource_inputs.on('change', function(){

			  	var elem = $(this);
			  	resource_id = elem.find(":selected").val();
			  	var resource_select_id = elem.attr('id');
			  	var resourceview_select_id = resource_select_id.replace('resource', 'resourceview');

			  	if ($('#'+resourceview_select_id+' option').length > 0)
			  		$('#'+resourceview_select_id).find('option').not(':first').remove();

			  	$('#' + resourceview_select_id + '_preview').html();

			  	api.get('montrose_resource_show_resource_views', {id: resource_id}).done(
			  		function(data){

			  			var opts = $('#'+resourceview_select_id);
						$.each( data.result, function(idx, elem) {
						    opts.append(new Option(elem.title, elem.id));
						});

						$('.'+resourceview_select_id).removeClass('hidden');
			  		});
				});



			// Resource views event handlers

			var resourceview_inputs = $('[id*=chart_resourceview_]');
			resourceview_inputs.on('change', function(){

			  	var elem = $(this);
			  	var resourceview_id = elem.find(":selected").val();
			  	var resourceview_select_id = elem.attr('id');

				var base_url = ckan.sandbox().client.endpoint;
			  	var src = base_url + '/dataset/' + dataset_name + '/resource/' + resource_id + '/view/' + resourceview_id;

			  	ckan.sandbox().client.getTemplate('iframe.html', {source: src})
			  	.done(function(data){
					console.log(data);
					$('#' + resourceview_select_id + '_preview').html();
					$('#' + resourceview_select_id + '_preview').html(data);
				});
			});
		});


		// Map select event handler

		$('#montrose_map').on('change', function(){

		  	if ($('#montrose_map_main_property option').length > 0)
		  		$('#montrose_map_main_property').empty();

			// Get resource id
			var resource_id = $('#montrose_map option:selected').val();
			var params = {id: resource_id};
			api.get('montrose_resource_show_map_properties', params)
			.done(function(data){

	  			var opts = $('#montrose_map_main_property');
				$.each( data.result, function(idx, elem) {
				    opts.append(new Option(elem.text, elem.value));
				});
				$('.montrose_map_main_property').removeClass('hidden');

			});
		});
	});
})($);