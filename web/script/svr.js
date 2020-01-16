$(document).ready(function(){
	$('#next_button').on('click',function(){
		var kernel = [];
		$.each($("[name = 'kernel']"), function(){
			if($(this).css('background-color') == 'rgb(91, 192, 222)') 
			{
				kernel.push($(this).html());
			}
		});
		kernel = kernel.join(',');
		
		var gamma = $('#gamma').val();
		var C = $('#C').val();
		var epsilon = $('#epsilon').val();
		
		alert(kernel);
		alert(gamma);
		alert(C);
		alert(epsilon);
	});
});