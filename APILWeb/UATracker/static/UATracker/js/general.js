$(document).ready(function(event) {
	
	$('#imageSearchForm').on('submit', function(event){
		event.preventDefault();
		window.history.pushState("object or string", "Title", "/uat/1/?"+$('#imageSearchForm').serialize());
		submitSearch();
	})
	if (document.location.hostname == "localhost"){
		$('#button').hide(0);

	}

	$('#i_file').change( function(event) {
		addFile();
		var tmppath = URL.createObjectURL(event.target.files[0]);
		    $("img").fadeIn("fast").attr('src',URL.createObjectURL(event.target.files[0]));

		    // $("#disp_tmp_path").html("Temporary Path(Copy it and try pasting it in browser address bar) --> <strong>["+tmppath+"]</strong>");
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

function openImport() {
	console.log("import dialog opened");

	$('#importDialog').css('visibility', 'visible');
	// $.ajax({
	// 	url: "http://127.0.0.1:8000/uat/1",
	// 	type: "GET",
	// 	data: "",
	// 	success: function(response) {
	// 		$('#dialogBox').append(response);
	// 	} ,
	// 	error:  function(x, y, z){}
	// });
}

function closeImport() {
	console.log("Import dialog closed");
	$('#importDialog').css('visibility','hidden');
}

function deleteItem() {
	var selection = document.getElementById("imageSequences");
	console.log( "item " + selection.options[ selection.selectedIndex ].value + " deleted");
}

function addFile() {
	console.log("file dialog opened");
	var newThing = document.getElementById('i_file').value;
	// $("#preview").fadeIn("fast").attr('src',URL.createObjectURL(event.target.files[0]));

		console.log("newThing grabbed"+newThing)
		if (newThing) {
			var startIndex = (newThing.indexOf('\\') >=0 ? newThing.lastIndexOf('\\') : newThing.lastIndexOf('/'));
			var filename = newThing.substring(startIndex);
			if (filename.indexOf('\\') === 0 || filename.indexOf('/') === 0) {
				filename = filename.substring(1);
			}
		}
		
		var str = document.getElementById('path').value;
		if (str.substr(str.length - 1) != '/'){
			str = str + '/';
		}
		var str = str + filename;
		$("#disp_tmp_path").html("Complete Path: <strong>"+str+"</strong>");

		

		
		// this is the part where we send the new thing to the database adder

}