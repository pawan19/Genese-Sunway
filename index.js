
function show()
{

	var NAME = document.getElementById("name").value;
	var ADD= document.getElementById("add").value;
	var EMAIL = document.getElementById("mail").value;
	var DESC = document.getElementById("description").value;
	var api= "https://x7nao3lrx9.execute-api.us-east-1.amazonaws.com/test/demo"


	var params = {
			"Name":NAME,
			"Address":ADD,
			"Email":EMAIL,
			"Description":DESC
	};

	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
	   	 if (this.readyState == 4 && this.status == 200) {
	       // Typical action to be performed when the document is ready:
	       alert(xhttp.responseText);
	    }
	};
	xhttp.open("POST", api, false);
	var a= xhttp.send(JSON.stringify(params));
	document.getElementById("name").value = '';
	document.getElementById("add").value = '';
	document.getElementById("mail").value = '';
	document.getElementById("description").value = '';


}
