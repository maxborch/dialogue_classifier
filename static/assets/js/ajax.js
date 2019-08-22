//Function is adapted from: https://www.youtube.com/watch?v=jKSNciGr8kY
$ (function(){

	$('#search').keyup(function() {
	
		$.ajax({
			type: "POST",
			url: "/data/search_results?short=True",
			data:{
				'search_item': $('#search').val(),
				'csrfmiddlewaretoken' : $('input[name="csrfmiddlewaretoken"]').val()	
			},
			success: searchSuccess,
			dataType: 'html'
		});
	});
});

function searchSuccess(data, textStatus, jqXHR)
{
	$('#search_results').html(data);
}
