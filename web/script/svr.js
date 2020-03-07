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

	$('#next_button').on('click', async function(){

		model_type = 'regression';
		model_name = 'svr';

		var dataset_files = {};
		dataset_files['train_file'] = document.getElementById('train_file').value;
		dataset_files['test_file'] = document.getElementById('test_file').value;

		var fail = 0;
		let status = await eel.check_file_exists(dataset_files['train_file'])();
		if(status != 'exist')
		{
			$('#train_file_info').html(status);
			fail = 1;
		}
		else
		{
			$('#train_file_info').html('');
			fail = 0;
		}
		status = await eel.check_file_exists(dataset_files['test_file'])();
		if(status != 'exist')
		{
			$('#test_file_info').html(status);
			fail = 1;
		}
		else
		{
			$('#test_file_info').html('');
			fail = 0;
		}
		if(fail == 1)
			return;

		var param = {};
		param['kernel'] = get_parameters_box('kernel', 'rbf');
		param['gamma'] = get_parameters_text('gamma', 'scale');
		param['C'] = get_parameters_text('C', '1.0')
		param['epsilon'] = get_parameters_text('epsilon', '0.1');

		window.location.replace('../web_frontend/display.html');

		eel.get_parameters(model_type, model_name, dataset_files, param);

	});
});
