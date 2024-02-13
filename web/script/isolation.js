$(document).ready(function(){

	$('#next_button').on('click', async function(){

		model_type = 'anomaly';
		model_name = 'isolation';

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

		empty_all_running_logs_anomaly();
		
		var param = {}
		param['n_estimators'] = get_parameters_text('n_estimators', '100');
		param['max_samples'] = get_parameters_text('min_samples', '256');
		param['contamination'] = get_parameters_text('contamination', '0.1');
		param['max_features'] = get_parameters_text('max_features', '1.0');
		param['bootstrap'] = get_radio_button_value_by_ids(['False', 'True']);

		classes_bar = await eel.get_parameters(model_type, model_name, dataset_files, param)();
		if(classes_bar != 'fail')
			plot_classes_bar(classes_bar);
		else
			model_fail_status();
	});
});