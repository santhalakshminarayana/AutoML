$(document).ready(function(){

	$('#next_button').on('click', async function(){

		model_type = 'classification';
		model_name = 'logistic';

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
		param['penalty'] = get_parameters_box('penalty', 'l2');
		param['C'] = get_parameters_text('C', '1.0');
		
		// recieves (model, evaluation_metrics, confusion_matrix)
		evaluation_plots = await eel.get_parameters(model_type, model_name, dataset_files, param)();
		if(evaluation_plots != 'fail')
		{
			plot_evaluation_metrics(evaluation_plots[0], evaluation_plots[1]);
			plot_confusion_matrix(evaluation_plots[2]);
		}
		else
			model_fail_status();
	});
});