$(document).ready(function(){

	function get_parameters_text(id, default_val)
	{
		var para = $('#' + id).val();
		if($.isEmptyObject(para))
			return default_val;
		else
			return para;
	}

	function get_parameters_box(name, default_val)
	{
		var para = [];
		$.each($("[name = " + name + "]"), function(){
			if($(this).css('background-color') == 'rgb(91, 192, 222)') 
				para.push($(this).html());
		});
		if($.isEmptyObject(para))
			return default_val;
		else
			return para.join(',');
	}

	$('#next_button').on('click',function(){

		var n_estimators = get_parameters_text('n_estimators', '10')
		var criterion = get_parameters_box('criterion', 'gini');
		var max_depth = get_parameters_text('max_depth', 'None')
		var min_samples_split = get_parameters_text('min_samples_split', '2')
		var max_features = get_parameters_box('max_features', 'auto');
		var max_leaf_nodes = get_parameters_text('max_leaf_nodes', 'None');
		var bootstrap = get_parameters_box('bootstrap', 'True');

		alert(n_estimators);
		alert(criterion);
		alert(max_depth);
		alert(min_samples_split);
		alert(max_features);
		alert(max_leaf_nodes);
		alert(bootstrap);

	});
});