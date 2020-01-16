$(document).ready(function(){

	function get_parameters(name)
	{
		var para = [];
		$.each($("[name = " + name + "]"), function(){
			if($(this).css('background-color') == 'rgb(91, 192, 222)') 
			{
				para.push($(this).html());
			}
		});
		return para.join(',');
	}

	$('#next_button').on('click',function(){

		var n_estimators = $('#n_estimators').val();
		var criterion = get_parameters('criterion');
		var max_depth = $('#max_depth').val();
		var min_samples_split = $('#min_samples_split').val();
		var max_features = get_parameters('max_features');
		var max_leaf_nodes = $('#max_leaf_nodes').val();
		var bootstrap = get_parameters('bootstrap');

		alert(n_estimators);
		alert(criterion);
		alert(max_depth);
		alert(min_samples_split);
		alert(max_features);
		alert(max_leaf_nodes);
		alert(bootstrap);

	});
});