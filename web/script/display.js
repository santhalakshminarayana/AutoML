$(document).ready(function(){
	
	eel.expose(update_succes_logs)
	async function update_success_logs(logs)
	{
		$('#dataset_logs').append(logs);
		$('#data_processing_result').append('Model build succesfully.');
	}

	eel.expose(update_fail_logs)
	async function update_fail_logs(dataset_type, logs)
	{
		$('#dataset_logs').append(logs);
		$('#data_processing_result').append('Model build failed due to improper' + dataset_type + 'dataset');
		$('#button').show();
	}
});