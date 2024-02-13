$(document).ready(function(){

	$('#next_button').on('click', async function(){

		model_type = 'regression';
		model_name = 'regression_random';

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

		empty_all_running_logs_regression();
		
		var param = {}
		param['n_estimators'] = get_parameters_text('n_estimators', '10');
		param['criterion'] = get_parameters_box('criterion', 'mse');
		param['max_depth'] = get_parameters_text('max_depth', 'None');
		param['min_samples_split'] = get_parameters_text('min_samples_split', '2');
		param['max_features'] = get_parameters_box('max_features', 'auto');
		param['max_leaf_nodes'] = get_parameters_text('max_leaf_nodes', 'None');
		param['bootstrap'] = get_parameters_box('bootstrap', 'True');

		// recieves (model, evaluation_metrics) 
		evaluation_metrics =  await eel.get_parameters(model_type, model_name, dataset_files, param)();
		if(evaluation_metrics != 'fail')
			plot_evaluation_metrics(evaluation_metrics[0], evaluation_metrics[1]);
		else
			model_fail_status();
	});
});