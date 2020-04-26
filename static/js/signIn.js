$(function(){
	$('#btnSignIn').click(function(){
		
		$.ajax({
			url: '/signIn',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log('success!!');
				console.log(response);
				window.location.href = '/products';
			},
			error: function(error){
				console.log('error :(');
				console.log(error);
			}
		});
	});
});
