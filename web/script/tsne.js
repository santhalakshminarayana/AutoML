$(document).ready(function(){

	$('#next_button').on('click', async function(){

		model_type = 'dimension';
		model_name = 'tsne';

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
		param['perplexity'] = get_parameters_text('perplexity', '30.0');
		param['learning_rate'] = get_parameters_text('learning_rate', '200.0');
		param['n_iter'] = get_parameters_text('n_iter', '250');
		param['n_iter_without_progress'] = get_parameters_text('n_iter_without_progress', '300');
		param['min_grad_norm'] = get_parameters_text('min_grad_norm', '0.0000001');
		param['metric'] = get_radio_button_value_by_ids(['euclidean', 'l1', 'l2', 'manhattan', 'cosine']);

		convergence = await eel.get_parameters(model_type, model_name, dataset_files, param)();
		if(convergence != 'fail')
			plot_convergence(convergence);
		else
			model_fail_status();
	});
});