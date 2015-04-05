function formValidator() {
	var f = document.getElementById("crmFile").value;
	if (f == null || f == '') {
		alert("Must attach file");
		return false;
	}
	var i = document.forms["crmForm"]["custom_audience_id"].value;
	if (i == null || i == "" || /[a-zA-Z]/.test(i)) {
		alert("Input external ID from AdRoll service");
		return false;
	}	
}
