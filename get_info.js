$(document).ready(function() {

  // Handle form submission.
  $("#submit").click(function(e) {

    var firstName = $("#firstName").val();

    e.preventDefault();
	



	  $.ajax({
		type: 'GET',
		url: 'https://7rzmjua15g.execute-api.ap-south-1.amazonaws.com/dev/getinfo/'+firstName,
		crossDomain: "true",
		contentType: 'application/json',
		success: function(res) {
		  console.log(res);
            alert("Contact Number: "+res.contactNumber + "\nName :"+res.Name + " "+res.SurName + "\nEmail " + res.emailId);
		},
		error: function(jqxhr, status, exception) {
		  $('#form-response').html('<div class="mt-3 alert alert-danger" role="alert">An error occurred. Please try again later.</div>');
		  $('#submit').text('Save preferences');
		  $('#submit').prop('disabled', false);
        }
      });
    
  });
});