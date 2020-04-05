$(document).ready(function(){

	$('#next_button').on('click', async function(){

		model_type = 'dimension';
		model_name = 'svd';

		var dataset_files = {};
		dataset_files['train_file'] = document.getElementById('train_file').value;

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
		
		if(fail == 1)
			return;

		empty_all_running_logs_dimension();
		
		var param = {}
		param['n_components'] = get_parameters_text('n_components', '2');
		param['n_iter'] = get_parameters_text('n_iter', '5');

		convergence = await eel.get_parameters(model_type, model_name, dataset_files, param)();
		if(convergence != 'fail')
			plot_convergence(convergence);
		else
			model_fail_status();
	});
});