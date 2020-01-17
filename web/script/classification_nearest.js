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
		var n_neighbors = get_parameters_text('n_neighbors', '5');
		var p = get_parameters_text('p', '2');
		
		alert(n_neighbors);
		alert(p);
	});
});