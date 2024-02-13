$(document).ready(function(){
	// hide welcom message
	var load_time = 2000;
	setTimeout(function(){
		$("#welcome").hide()},load_time);
	setTimeout(function(){
		$("#main").show()},load_time);

	// zehero section
	$('.zehero').click(function(){
		$('.sub-menu').hide();
		$('.menu_block').css('background-color','transparent');
		// change all sub-menu item colors to normal color
		var nor_clr = '#F1D3BC';
		$('.sub-menu a').css('color', nor_clr);
	});

	// hide-show sub-menu, change background color
	$('.sub-menu').hide();
	$('div ul li.menu_block').click(function(){
		var clr = '#F35A4A';
		var menu_block_ids = ['#regressor', '#classifier', '#clustering', '#anomaly', '#dimension']
		$.each(menu_block_ids, function(index, value){
			$(value).css('background-color', 'transparent');
		});
		$('.sub-menu').hide();
		$(this).css('background-color',clr);
		$('.sub-menu', this).show();
	});

	// change color sub-menu selected item
	$('.sub-menu a').click(function(){
		// change all sub-menu item colors to normal color
		var nor_clr = '#F1D3BC';
		$('.sub-menu a').css('color', nor_clr);
		// change current selcted item color
		var clr = '#615049';
		$(this).css('color', clr);
	});
});
