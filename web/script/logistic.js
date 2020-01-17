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
		var penalty = get_parameters_box('penalty', 'l2');
		var C = get_parameters_text('C', '1.0')
		
		alert(penalty);
		alert(C);
	});
});