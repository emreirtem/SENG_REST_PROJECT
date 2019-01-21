
var updateStudentList = function(){
	StudentService.getAllStudents().then(r=>getStudentsCallback(r))
}

var updateAdvisorList = function(){
	AdvisorService.getAllAdvisors().then(r=>getAdvisorsCallback(r))
}

var addStudentCallback = function(r){
	if(r["success"]){
		$( "#student_id" ).val("");
		$( "#student_name" ).val("");
		updateStudentList();
		alert("Student added.");
	}else{
		alert(r["desc"]);
	}
}

var addAdvisorCallback = function(r){
	if(r["success"]){
		$( "#advisor_id" ).val("")
		$( "#advisor_name" ).val("")
		$( "#field_of_interest" ).val("")
		$( "#availability" ).val("")
		updateAdvisorList();
		alert("Advisor added.");
	}else{
		alert(r["desc"]);
	}
}

var getStudentsCallback = function(r){
	$("#student_list").html('<h4>Student List</h4>')
	for(i in r){
		$( "#student_list").append( '<button type="button" class="list-group-item list-group-item-action">'+r[i]["student_id"]+' - '+r[i]["student_name"]+'</button>' );
	}	
}
var getAdvisorsCallback = function(r){
	$("#advisor_list").html('<h4>Advisor List</h4>')
	for(i in r){
		$( "#advisor_list").append( '<button type="button" class="list-group-item list-group-item-action">'+r[i]["advisor_id"]+' - '+r[i]["advisor_name"]+'</button>' );
	}	
}

$( "#submit_student" ).click(function() {
	student_id = $( "#student_id" ).val()
	student_name = $( "#student_name" ).val()
	StudentService.createStudent(student_id, student_name).then(r=>addStudentCallback(r))
});

$( "#submit_advisor" ).click(function() {
	advisor_id = $( "#advisor_id" ).val()
	advisor_name = $( "#advisor_name" ).val()
	field_of_interest = $( "#field_of_interest" ).val()
	availability = $( "#availability" ).val()
	AdvisorService.createAdvisor(advisor_id, advisor_name, field_of_interest, availability).then(r=>addAdvisorCallback(r))
});

$( document ).ready(function() {
    updateStudentList();
	updateAdvisorList();
});