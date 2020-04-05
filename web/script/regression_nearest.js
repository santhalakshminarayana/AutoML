$(document).ready(function(){

	$('#next_button').on('click', async function(){
		
		model_type = 'regression';
		model_name = 'regression_nearest';

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
		param['n_neighbors'] = get_parameters_text('n_neighbors', '5');
		param['p'] = get_parameters_text('p', '2');
		
		// recieves (model, evaluation_metrics) 
		evaluation_metrics =  await eel.get_parameters(model_type, model_name, dataset_files, param)();
		if(evaluation_metrics != 'fail')
			plot_evaluation_metrics(evaluation_metrics[0], evaluation_metrics[1]);
		else
			model_fail_status();
		
	});

});