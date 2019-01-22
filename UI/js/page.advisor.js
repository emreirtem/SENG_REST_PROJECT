var updateProfile=function(advisor_id){
	AdvisorService.getAdvisorById(advisor_id)
		.then(function(r){
			$("#profile #advisor_name").text(r["advisor_name"]);
			$("#profile #advisor_id").text(r["advisor_id"]);
			if(r["availability"]){
				$("#profile #advisor_availability").text("Available");
			}else{
				$("#profile #advisor_availability").text("Unavailable");
			}
			$("#profile #field_of_interest").text(r["field_of_interest"]);
		})
	
}
$( "#login_form #login" ).click(function() {
	advisor_id = $( "#advisor_id" ).val()
	AdvisorService.validateAdvisorById(advisor_id)
		.then(function(r){
			if(r["isAdvisorValid"]){
				updateProfile($( "#advisor_id" ).val())
			}else{
				alert("Advisor Id is invalid")
			}
		});
});

$(".update_available").click(function(){
	advisor_id = $( "#profile #advisor_id" ).text()
	value = $(this).attr("data-value")
	AdvisorService.updateAvailability(advisor_id, value)
		.then(function(r){
			if(r["success"]){
				advisor_id = $( "#profile #advisor_id" ).text();
				updateProfile(advisor_id);
			}else{
				alert(r["desc"])
			}
		})
});




