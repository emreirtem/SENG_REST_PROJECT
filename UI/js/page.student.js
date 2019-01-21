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

var validateStudentCallback = function(r){
	if(r["isStudentValid"]){		
		student_id = $( "#student_id" ).val()
		StudentService.getStudentById(student_id).then(r=>getStudentByIdCallback(r))		
	}else{
		alert("Invalid user.");
	}
}  

var getStudentByIdCallback = function(r){			
		$("#student_name").text(r["student_name"]);	
} 


$( "#login" ).click(function() {
	student_id = $( "#student_id" ).val()
	if (!validation.isNumber(student_id)){
		alert('Student id must be a number.')
	} else {
		StudentService.validateStudentById(student_id).then(r=>validateStudentCallback(r))
	}
});


$( "#choose_advisor" ).click(function() {
	AdvisorService.getAllAdvisors().then(r=>getAllAdvisorsCallback(r))
});


var getAllAdvisorsCallback = function(r){
	alert(JSON.stringify(r))
	for (i in r) {
		$( "#advisor_list_group").append( '<button type="button" class="list-group-item list-group-item-action">'+r[i]["advisor_id"]+' - '+r[i]["advisor_name"]+'</button>' );
	
	}	
		

} 



