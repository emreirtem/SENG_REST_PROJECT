var validation = {
    isNotEmpty:function (str) {
        var pattern =/\S+/;
        return pattern.test(str);  // returns a boolean
    },
    isNumber:function(str) {
        var pattern = /^\d+$/;
        return pattern.test(str);  // returns a boolean
    },
    isSame:function(str1,str2){
        return str1 === str2;
    }
};


$( "#login" ).click(function() {
	student_id = $( "#student_id" ).val()
	if (!validation.isNumber(student_id)){
		alert('Student id must be a number.')
	} else {
		StudentService.validateStudentById(student_id)
		.then(function(r){
				if(r["isStudentValid"]){		
					student_id = $( "#student_id" ).val()
					StudentService.getStudentById(student_id)
					.then(
						function(r){
							$("#student_name").text(r["student_name"])		
							
							if (r["approval_status"] == "ACCEPT_WAITING") {
								// if waiting for approval, no topic, no advisor button
								AdvisorService.getAdvisorById(r["advisor_id"]).then(r=>$( "#advisor_name" ).text(r["advisor_name"]))
								r["approval_status"] = "WAITING FOR ACCEPTANCE"
								r["thesis_topic"] = "You can decide the topic after advisor approval"
								$( "#choose_advisor" ).hide()
								$( "#choose_topic" ).hide()
							} else if (r["approval_status"] == "ACCEPTED"){
								// if approval accepted, no advisor button only topic button
								AdvisorService.getAdvisorById(r["advisor_id"]).then(r=>$( "#advisor_name" ).text(r["advisor_name"]))
								if (r["thesis_topic"] == null) {
									r["thesis_topic"] = "Not Determined Yet"
								}
								$( "#choose_advisor" ).hide();
								$( "#choose_topic" ).show()								
								
							} else if (r["approval_status"] == "REJECTED"){
								// if approval rejected, only advisor button
								AdvisorService.getAdvisorById(r["advisor_id"]).then(r=>$( "#advisor_name" ).text(r["advisor_name"]))
								r["thesis_topic"] = "You can decide the topic after advisor approval"
								$( "#choose_advisor" ).show();
								$( "#choose_topic" ).hide()
							} else {
								// if none of above, only advisor button, student didnt choose anything yet
								$( "#advisor_name" ).text("Advisor is not determined yet.")
								r["approval_status"] = " - "
								r["thesis_topic"] = "Please determine an advisor first."
								$( "#choose_advisor" ).show();
								$( "#choose_topic" ).hide()
							}		
							
							$( "#approval_status" ).text(r["approval_status"])							
							$( "#thesis_topic" ).text(r["thesis_topic"])							
						}
					)	
					
				}else{
					alert("Invalid user.");
				}
			})
	}
});


$( "#choose_advisor" ).click(function() {
	AdvisorService.getAllAdvisors()
	.then(function(r){
				$("#advisor_list_group").html('<h1>Advisors List</h1>')
				for (i in r) {	
					if (r[i]["availability"]) {
						var availability = 'Available'
					} else {
						var availability = 'Not Available'
					}
					
					if (r[i]["field_of_interest"] == null) {
						r[i]["field_of_interest"] = 'No field of interest'
					}
					$( "#advisor_list_group").append( '<button type="button" class="list-group-item list-group-item-action choose-advisor" data-id="'+r[i]["advisor_id"]+'">'+r[i]["advisor_id"]+' - '+r[i]["advisor_name"]+' - '+availability+' - '+r[i]["field_of_interest"]+'</button>' );
				}
			}
		)
});

$(document).on('click', '.choose-advisor', function(){ 
	advisor_id = $(this).attr("data-id")
	student_id = $( "#student_id" ).val()
	
	StudentService.sendApprovalRequest(student_id, advisor_id)
	.then(
		function(r){
			if (r["success"]) {
				alert(" choose advisor success")
			} else {
				if (r["remoteAdvisorService"] == null) {
					alert(r["desc"])
				} else {
					alert(r["remoteAdvisorService"]["desc"])
				}			
			}
		})	
});


$( "#send_topic" ).click(function() {
	thesis_topic_area = $( "#thesis_topic_area" ).val()
	alert(thesis_topic_area)
});





