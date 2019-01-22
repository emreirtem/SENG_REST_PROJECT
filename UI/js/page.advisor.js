var updateProfile=function(advisor_id){
	$("#student_card").hide()
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
		});
	AdvisorService.getApprovalRequestsOfAdvisor(advisor_id)
		.then(function(r){
				$( "#approval_requests").html("")
				for(i in r){
					StudentService.getStudentById(r[i]["student_id"])
						.then(function(r){
							$( "#approval_requests")
								.append('<li class="list-group-item" class="approval_request" data-id="'+r["student_id"]+'">'
								+'<button type="button" class="btn btn-success btn-sm request_accept">✔</button> '
								+'<button type="button" class="btn btn-danger btn-sm request_reject">✖</button> '
								+ r["student_name"]+'</li>' );
						})
				}
		});
	AdvisorService.getAcceptedStudentsOfAdvisor(advisor_id)
		.then(function(r){
			$( "#accepted_students").html("")
			for(i in r){
				StudentService.getStudentById(r[i]["student_id"])
						.then(function(r){
							$( "#accepted_students")
							.append('<button type="button" class="list-group-item'+
							' list-group-item-action accepted_student" data-id="'+r["student_id"]+'">'
							+r["student_name"]+'</button>' );
						})
			}
		});
		
}
$( "#login_form #login" ).click(function() {
	advisor_id = $( "#advisor_id" ).val()
	AdvisorService.validateAdvisorById(advisor_id)
		.then(function(r){
			if(r["isAdvisorValid"]){
				updateProfile($( "#advisor_id" ).val());
				manager.active("#profile")
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


$(document).on("click",".request_accept", function(){
	advisor_id = $( "#profile #advisor_id" ).text();
	student_id = $(this).parent().attr("data-id");
	AdvisorService.acceptApprovalRequest(advisor_id, student_id)
		.then(function(r){
			advisor_id=$( "#profile #advisor_id" ).text()
			updateProfile(advisor_id)
		})
});
$(document).on("click",".request_reject", function(){
	advisor_id = $( "#profile #advisor_id" ).text();
	student_id = $(this).parent().attr("data-id");
	AdvisorService.rejectApprovalRequest(advisor_id, student_id)
		.then(function(r){
			advisor_id=$( "#profile #advisor_id" ).text()
			updateProfile(advisor_id)
		})
});

$(document).on("click",".accepted_student", function(){
	student_id = $(this).attr("data-id");
	StudentService.getStudentById(student_id)
		.then(function(r){
			$("#adv_student_id").text(r["student_id"])
			$("#adv_student_name").text(r["student_name"])
			$("#adv_topic").text(r["thesis_topic"])
			$("#student_card").show()
		})
});
manager = new DisplayManager(["#profile", "#login_form"])

$(document).ready(function(){
	manager.active("#login_form")
	
});


