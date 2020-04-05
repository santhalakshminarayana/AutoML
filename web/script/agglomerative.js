$(document).ready(function(){

	$('#next_button').on('click', async function(){

		model_type = 'clustering';
		model_name = 'agglomerative';

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

		empty_all_running_logs_clustering();
		
		var param = {}
		param['n_clusters'] = get_parameters_text('n_clusters', '2');
		param['affinity'] = get_radio_button_value_by_ids(['euclidean', 'l1', 'l2', 'manhattan', 'cosine']);
		param['linkage'] = get_radio_button_value_by_ids(['average', 'complete', 'single']);

		classes_bar = await eel.get_parameters(model_type, model_name, dataset_files, param)();
		if(classes_bar != 'fail')
			plot_classes_bar(classes_bar);
		else
			model_fail_status();
	});
});