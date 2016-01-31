var beginID;
var endID;
var selecting;
$(document).ready(function(event) {
	
	$('#imageSearchForm').on('submit', function(event){
		event.preventDefault();
		var serialized = $('#imageSearchForm').serialize();
		serialized = serialized.replace("tracers=m","tracers=3");
		window.history.pushState("object or strin", "Title", "/uat/1/?"+serialized);
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
	activateRowSelection();
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
}

function activateRowSelection(){
	$('.mainTableRow').mousedown(function(e) {
		e.preventDefault();
		if( e.button == 0){
			selecting = true;
			beginID = $(this).index();
			$(this).css({"background-color":"#aaf"});
			$(this).data("selected",true);
		}
	});
	$('.mainTableRow').mouseenter(function() {
		if(selecting == true){
			endID = $(this).index();
			if( parseInt(beginID) >= parseInt(endID)){
				var temp = beginID;
				beginID = endID;
				endID = temp;
			}
			for(i=beginID;i<endID;i++){
				$('.mainTableRow').eq(i).css({"background-color":"#aaf"});
				$('.mainTableRow').eq(i).data("selected",true);
			}
		}
	});
	$('.mainTableRow').mouseup(function(e){
		if( e.button == 2 && $(this).data("selected")==true){
			e.preventDefault();
			xx = e.pageX+"px";
			yy = e.pageY+"px";
			console.log(xx);
			console.log(yy);
			console.log('--------');
			$("#rightClickMenu").css({top: yy, left: xx});
			$('#rightClickMenu').css('visibility','visible');
		} 
	});
	$(document).mouseup(function(e) {
		selecting = false;
	});
	$(document).mousedown(function(e) {
		$('#rightClickMenu').css('visibility','hidden');
	});
}