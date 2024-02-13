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

function get_radio_button_value_by_ids(radio_button_ids)
{
	for(i = 0; i < radio_button_ids.length; i++)
	{
		selected_value = $('#' + radio_button_ids[i]).is(':checked');
		if(selected_value)
			return radio_button_ids[i];
	}
	return radio_button_ids[0];
}

eel.expose(update_pass_logs)
function update_pass_logs(dataset_type, logs)
{
	$('#dataset_logs').append(logs);
	$('#data_processing_result').append(dataset_type + ' dataset read succesfully.');
}

eel.expose(update_fail_logs)
function update_fail_logs(dataset_type, logs)
{	
	$('#dataset_logs').append(logs);
	$('#data_processing_result').append('Dataset reading failed due to improper ' + dataset_type + ' dataset');
	return
}

function empty_all_running_logs_regression()
{
	$('#logs').show();
	$('#dataset_logs').text('');
	$('#data_processing_result').text('');
	$('#model_fail_status').hide();
	$('#model').hide();
	$('#best_model').text('');
	$('#plots').hide()
	$('#training_data_evaluation').attr('src', '');
	$('#evaluation_data_evaluation').attr('src', '');
}

function empty_all_running_logs_classification()
{
	$('#logs').show();
	$('#dataset_logs').text('');
	$('#data_processing_result').text('');
	$('#model_fail_status').hide();
	$('#model').hide();
	$('#best_model').text('');
	$('#plots').hide();
	$('#training_data_evaluation').attr('src', '');
	$('#evaluation_data_evaluation').attr('src', '');
	$('#training_data_confusion_matrix').attr('src', '');
	$('#evaluation_data_confusion_matrix').attr('src', '');
}

function empty_all_running_logs_clustering()
{
	$('#logs').show();
	$('#dataset_logs').text('');
	$('#data_processing_result').text('');
	$('#model_fail_status').hide();
	$('#plots').hide();
	$('#predicted_classes_plot').attr('src', '');
}

function empty_all_running_logs_anomaly()
{
	$('#logs').show();
	$('#dataset_logs').text('');
	$('#data_processing_result').text('');
	$('#model_fail_status').hide();
	$('#plots').hide();
	$('#predicted_classes_plot').attr('src', '');
}

function empty_all_running_logs_dimension()
{
	$('#logs').show();
	$('#dataset_logs').text('');
	$('#data_processing_result').text('');
	$('#model_fail_status').hide();
	$('#plots').hide();
	$('#convergence_plot').attr('src', '');
}

function plot_evaluation_metrics(model, evaluation_metrics)
{
	$('#model').show();
	$('#best_model').append(model);
	$('#plots').show();
	$('#training_data_evaluation').attr('src', evaluation_metrics[0]);
	$('#evaluation_data_evaluation').attr('src', evaluation_metrics[1]);
}

function plot_confusion_matrix(confusion_matrix)
{
	$('#training_data_confusion_matrix').attr('src', confusion_matrix[0]);
	$('#evaluation_data_confusion_matrix').attr('src', confusion_matrix[1]);
}

function plot_classes_bar(classes_bar)
{
	$('#plots').show();
	$('#predicted_classes_plot').attr('src', classes_bar);
}

function plot_convergence(convergence)
{
	$('#plots').show();
	$('#convergence_plot').attr('src', convergence);
}

function model_fail_status()
{
	$('#model_fail_status').show();
}