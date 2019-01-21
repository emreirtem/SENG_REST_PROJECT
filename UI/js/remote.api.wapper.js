const REMOTE_STUDENT_SERVICE_URI = 'http://127.0.0.1:5000/student/'
const REMOTE_ADVISOR_SERVICE_URI = 'http://127.0.0.1:5001/advisor/'
var uri_builder = {
  student: {
    getAllStudents:function () {
      return REMOTE_STUDENT_SERVICE_URI + 'all'
    },
    createStudent: function () {
      return REMOTE_STUDENT_SERVICE_URI + 'new'
    },
    getStudentById: function (student_id) {
      return REMOTE_STUDENT_SERVICE_URI + student_id
    },
    validateStudentById: function (student_id) {
      return REMOTE_STUDENT_SERVICE_URI + student_id + '/validate'
    },
    sendApprovalRequest: function (student_id, advisor_id) {
      return REMOTE_STUDENT_SERVICE_URI + student_id + '/approval/send/' + advisor_id
    },
    triggerApprovalAcceptedEvent: function () {
      alert('sendApprovalRequest: AdvisorService automatically use this api')
    },
    triggerApprovalRejectedEvent: function () {
      alert('sendApprovalRequest: AdvisorService automatically use this api')
    },
    updateThesisTopic(student_id, thesis_topic) {
      return REMOTE_STUDENT_SERVICE_URI + student_id + '/thesis_topic/' + thesis_topic
    }
  },
  advisor: {
	  validateAdvisorById:function(advisor_id){
		  return REMOTE_ADVISOR_SERVICE_URI + advisor_id + "/validate"
	  },
	  isAdvisorAvailable: function(advisor_id){
		  return REMOTE_ADVISOR_SERVICE_URI + advisor_id + "/is_available"
	  },
	  getAllAdvisors:function(){
		  return REMOTE_ADVISOR_SERVICE_URI + "all"
	  },
	  getAdvisorById: function(advisor_id){
		  return REMOTE_ADVISOR_SERVICE_URI + advisor_id
	  },
	  createAdvisor:function(){
		  return REMOTE_ADVISOR_SERVICE_URI + "new"
	  },
	  updateAvailability:function(advisor_id, availability_status){
		  if(availability_status==true){
			  availability_status="True"
		  }else{
			  availability_status="False"
		  }
		  return REMOTE_ADVISOR_SERVICE_URI + advisor_id + "/update_availability/" + availability_status
	  },
	  sendApprovalRequest:function(){
		  alert('sendApprovalRequest: StudentService automatically use this api')
	  },
	  acceptApprovalRequest:function(advisor_id, student_id){
		  return REMOTE_ADVISOR_SERVICE_URI + advisor_id + "/approval/request/"+student_id+"/accept"
	  },
	  rejectApprovalRequest:function(advisor_id, student_id){
		  return REMOTE_ADVISOR_SERVICE_URI + advisor_id + "/approval/request/"+student_id+"/reject"
	  },
	  getAcceptedStudentsOfAdvisor:function(advisor_id){
		  return REMOTE_ADVISOR_SERVICE_URI + advisor_id + "/approval/all"
	  },
	  getApprovalRequestsOfAdvisor:function(advisor_id){
		  return REMOTE_ADVISOR_SERVICE_URI + advisor_id + "/approval/requests"
	  }
  }
}


var StudentService={
	getAllStudents:function(){
		return fetch(uri_builder.student.getAllStudents())
		  .then(function(response) {
			return response.json();
		  })
	},
    createStudent: function(student_id, student_name) {
		var formData = new FormData();
		formData.append('student_id', student_id);
		formData.append('student_name', student_name);
		formData.append('advisor_id', "");
		formData.append('approval_status', "");
		formData.append('thesis_topic', "");
		
      return fetch(uri_builder.student.createStudent(),{
		  method: 'POST',
		  body: formData
		  }).then(function(response) {
			  return response.json();
		  });
    },
    getStudentById: function (student_id) {
      return fetch(uri_builder.student.getStudentById(student_id))
		  .then(function(response) {
			return response.json();
		  });
    },
    validateStudentById: function (student_id) {
      return fetch(uri_builder.student.validateStudentById(student_id))
		  .then(function(response) {
			return response.json();
		  });
    },
    sendApprovalRequest: function (student_id, advisor_id) {
      return fetch(uri_builder.student.sendApprovalRequest(student_id, advisor_id),
		{method: 'PATCH'}).then(function(response) {
			return response.json();
		  });
    },
    triggerApprovalAcceptedEvent: function () {
      alert('sendApprovalRequest: AdvisorService automatically uses this api')
    },
    triggerApprovalRejectedEvent: function () {
      alert('sendApprovalRequest: AdvisorService automatically uses this api')
    },
    updateThesisTopic(student_id, thesis_topic) {
      return fetch(uri_builder.student.updateThesisTopic(student_id, thesis_topic),
	  {method: 'PATCH'}).then(function(response) {
			return response.json();
		  });
    }
}

var AdvisorService={
	validateAdvisorById:function(advisor_id){
		  return fetch(uri_builder.advisor.validateAdvisorById(advisor_id))
		  .then(function(response) {
			return response.json();
		  });
	  },
	  isAdvisorAvailable: function(advisor_id){
		  return fetch(uri_builder.advisor.isAdvisorAvailable(advisor_id))
		  .then(function(response) {
			return response.json();
		  });
	  },
	  getAllAdvisors:function(){
		  return fetch(uri_builder.advisor.getAllAdvisors())
		  .then(function(response) {
			return response.json();
		  });
	  },
	  getAdvisorById: function(advisor_id){
		  return fetch(uri_builder.advisor.getAdvisorById(advisor_id))
		  .then(function(response) {
			return response.json();
		  });
	  },
	  createAdvisor:function(advisor_id, advisor_name, field_of_interest, availability_status){
		  if(availability_status==true){
			  availability_status="True"
		  }else{
			  availability_status="False"
		  }
		  var formData = new FormData();
			formData.append('advisor_id', advisor_id);
			formData.append('advisor_name', advisor_name);
			formData.append('field_of_interest', field_of_interest);
			formData.append('availability_status', availability_status);
			
		  return fetch(uri_builder.advisor.createAdvisor(),{
			  method: 'POST',
			  body: formData
			  }).then(function(response) {
				  return response.json();
			  });
	  },
	  updateAvailability:function(advisor_id, availability_status){
		  return fetch(uri_builder.advisor.updateAvailability(advisor_id, availability_status),
			{method: 'PATCH'}).then(function(response) {
				return response.json();
			  });
	  },
	  sendApprovalRequest:function(){
		  alert('sendApprovalRequest: StudentService automatically use this api')
	  },
	  acceptApprovalRequest:function(advisor_id, student_id){
		  return fetch(uri_builder.advisor.acceptApprovalRequest(advisor_id, student_id),
			{method: 'PATCH'}).then(function(response) {
				return response.json();
			  });
	  },
	  rejectApprovalRequest:function(advisor_id, student_id){
		  return fetch(uri_builder.advisor.rejectApprovalRequest(advisor_id, student_id),
			{method: 'PATCH'}).then(function(response) {
				return response.json();
			  });
	  },
	  getAcceptedStudentsOfAdvisor:function(advisor_id){
		  return fetch(uri_builder.advisor.getAcceptedStudentsOfAdvisor(advisor_id))
		  .then(function(response) {
				return response.json();
			  });
	  },
	  getApprovalRequestsOfAdvisor:function(advisor_id){
		  return fetch(uri_builder.advisor.getApprovalRequestsOfAdvisor(advisor_id))
		  .then(function(response) {
				return response.json();
			  });
	  }
	
}
function service_help(){
	console.log("*****************************")
	console.log("*** STUDENT SERVICE LIST ****")
	console.log("*****************************")
	console.log("StudentService.getAllStudents().then(r=>console.log(JSON.stringify(r)))")
	console.log("StudentService.createStudent(student_id, student_name).then(r=>console.log(JSON.stringify(r)))")
	console.log("StudentService.getStudentById(student_id).then(r=>console.log(JSON.stringify(r)))")
	console.log("StudentService.validateStudentById(student_id).then(r=>console.log(JSON.stringify(r)))")
	console.log("StudentService.sendApprovalRequest(student_id, advisor_id).then(r=>console.log(JSON.stringify(r)))")
	console.log("StudentService.updateThesisTopic(student_id, thesis_topic).then(r=>console.log(JSON.stringify(r)))")
	console.log("*****************************")
	console.log("*** ADVISOR SERVICE LIST ****")
	console.log("*****************************")
	console.log("AdvisorService.validateAdvisorById(advisor_id).then(r=>console.log(JSON.stringify(r)))")
	console.log("AdvisorService.isAdvisorAvailable(advisor_id).then(r=>console.log(JSON.stringify(r)))")
	console.log("AdvisorService.getAllAdvisors().then(r=>console.log(JSON.stringify(r)))")
	console.log("AdvisorService.createAdvisor(advisor_id, advisor_name, field_of_interest, availability_status).then(r=>console.log(JSON.stringify(r)))")
	console.log("AdvisorService.updateAvailability(advisor_id,availability_status).then(r=>console.log(JSON.stringify(r)))")
	console.log("AdvisorService.sendApprovalRequest(advisor_id, student_id).then(r=>console.log(JSON.stringify(r)))")
	console.log("AdvisorService.acceptApprovalRequest(advisor_id, student_id).then(r=>console.log(JSON.stringify(r)))")
	console.log("AdvisorService.rejectApprovalRequest(advisor_id, student_id).then(r=>console.log(JSON.stringify(r)))")
	console.log("AdvisorService.getAcceptedStudentsOfAdvisor(advisor_id).then(r=>console.log(JSON.stringify(r)))")
	console.log("AdvisorService.getApprovalRequestsOfAdvisor(advisor_id).then(r=>console.log(JSON.stringify(r)))")
	console.log("------------------------------")
	console.log("type service_help() to list services")
}
service_help()