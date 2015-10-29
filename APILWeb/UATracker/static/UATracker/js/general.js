$(document).ready(function(event) {
	
	$('#imageSearchForm').on('submit', function(event){
		event.preventDefault();
		window.history.pushState("object or strin", "Title", "/uat/1/?"+$('#imageSearchForm').serialize());
		submitSearch();
	})
});
function submitSearch() {
	    $.ajax({
	        url : "../handle-search/1/", // the endpoint
	        type : "GET", // http method
	        data : $('#imageSearchForm').serialize(), 
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
