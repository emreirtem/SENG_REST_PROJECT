var updateStudentList = function(r){
	$( "#student_list").append( "<p>Test</p>" );
}

var addStudentCallback = function(r){
	if(r["success"]){
		$( "#student_id" ).val("");
		$( "#student_name" ).val("");
		alert("Student added.");
	}else{
		alert(r["desc"]);
	}
}

$( "#submit_student" ).click(function() {
	student_id = $( "#student_id" ).val()
	student_name = $( "#student_name" ).val()
	StudentService.createStudent(student_id, student_name).then(r=>addStudentCallback(r))
});

$( "#submit_advisor" ).click(function() {
	$( "#advisor_id" ).val("id")
	$( "#advisor_name" ).val("name")
	$( "#field_of_interest" ).val("field of interest")
	$( "#availability" ).val("availability")
	alert( "submit_student" );
});