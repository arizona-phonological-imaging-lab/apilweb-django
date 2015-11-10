$(document).ready(function(event) {
	
	$('#imageSearchForm').on('submit', function(event){
		event.preventDefault();
		var serialized = $('#imageSearchForm').serialize();
		serialized = serialized.replace("tracers=m","tracers=3");
		window.history.pushState("object or strin", "Title", "/uat/1/?"+serialized);
		submitSearch();
	})
});
function submitSearch() {
		var serialized = $('#imageSearchForm').serialize();
		serialized = serialized.replace("tracers=m","tracers=3");
		console.log(serialized);
	    $.ajax({
	        url : "../handle-search/1/", // the endpoint
	        type : "GET", // http method
	        data : serialized, 
	        // handle a successful response
	        success : function(newCode) {
	        	$('.mainTable').remove();
	        	$( ".searchBox" ).after(newCode);
	        },

	        // handle a non-successful response
	        error : function(xhr,errmsg,err) {
	            console.log("ERROR: "+errmsg)
	        }
	    });
};
