$(document).ready(function(){
	
	eel.expose(update_pass_logs)
	function update_pass_logs(logs)
	{
		$('#dataset_logs').append(logs);
		$('#data_processing_result').append('Model build succesfully.');
	}

	eel.expose(update_fail_logs)
	function update_fail_logs(dataset_type, logs)
	{
		alert('I got this');
		console.log(logs);
		$('#dataset_logs').append(logs);
		$('#data_processing_result').append('Model build failed due to improper' + dataset_type + 'dataset');
		return
	}

	$('#back_button').click(function(){
		window.history.go(-1); 
		return false;
	})

});