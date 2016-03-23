var beginID;
var endID;
var selecting;
var bpsc = 1; //Buffer Panel Selection Counter
var imagesToBeManipulated = [];


$(document).ready(function(event) {
	
	$('#imageSearchForm').on('submit', function(event){
		event.preventDefault();
		var serialized = $('#imageSearchForm').serialize();
		serialized = serialized.replace("tracers=m","tracers=3");
		window.history.pushState("object or strin", "Title", "/uat/1/?"+serialized);
		submitSearch();
	})

	$('#importDialogForm').on('submit', function(event){
		event.preventDefault();
		var serialized = $('#imageSearchForm').serialize();
		serialized = serialized.replace("tracers=m","tracers=3");
		window.history.pushState("object or strin", "Title", "/uat/1/?"+serialized);
		submitImport();
	})


	$('#i_file').change( function(event) {
		addFile();
		var tmppath = URL.createObjectURL(event.target.files[0]);
		    $("img").fadeIn("fast").attr('src',URL.createObjectURL(event.target.files[0]));

		    // $("#disp_tmp_path").html("Temporary Path(Copy it and try pasting it in browser address bar) --> <strong>["+tmppath+"]</strong>");
	})
	activateRowSelection();
	//Set up ajax to accomodate to Django's security demands:
	var csrftoken = getCookie('csrftoken');
	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }
	    }
	});
	prepareDialogBoxes();
});
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function submitSearch() {
		var serialized = $('#imageSearchForm').serialize();
		serialized = serialized.replace("tracers=m","tracers=3");
    $.ajax({
        url : "../handle-search/1/",
        type : "GET", // http method
        data : serialized, 
        // handle a successful response
        success : function(newCode) {
        	$('.mainTable').remove();
        	$( ".searchBox" ).after(newCode);
        	activateRowSelection();
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("ERROR: "+errmsg)
        }
    });
};

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
			$("#rightClickMenu").css({top: yy, left: xx});
			$('#rightClickMenu').css('visibility','visible');
		} 
	});
	$(document).mouseup(function(e) {
		selecting = false;
		$('.dropdownMenu').css('visibility','hidden');
	});
	$(document).mousedown(function(e) {
		//If the click is not inside the right click menu:
		if (e.target.id != "rightClickMenu" && !$(e.target).parents("#rightClickMenu").size()) {
			$('#rightClickMenu').css('visibility','hidden');
		}
	});
}

function clickedOnNextOrPrev(offset){
	//The offset is either 1 or -1 (next or prev).
	//It gets really hairy here. I use the html content for page number to retrieve the current page number.
	//And I use js regex which is not a very user friendly thing anyway. 
	var currentAddress = document.URL;
	var myRegex = /[^0-9]*(\d+).*/;
	var match = myRegex.exec($('#current').html());
	var currentPage = match[1];
	var nextPage = String(parseInt(currentPage)+offset);
	var newAddress = currentAddress.replace(/uat\/\d+/,"uat/"+nextPage);
	window.history.pushState("object or strin", "Title", newAddress);
	var callAddress = newAddress.replace("/uat/","/uat/handle-search/");
	$.ajax({
        url : callAddress,
        type : "GET",
        // handle a successful response
        success : function(newCode) {
        	$('.mainTable').remove();
        	$( ".searchBox" ).after(newCode);
        	activateRowSelection();
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("ERROR: "+errmsg)
        }
    });
    
}
function reloadTable(){
	var currentAddress = document.URL;
	if (currentAddress.indexOf("theTitle") > -1){
	//i.e. If no search has been performed so far and the URL does not have GET parameters:
		currentAddress += "?"+$('#imageSearchForm').serialize();
	} 
	var callAddress = currentAddress.replace("/uat/","/uat/handle-search/");
	$.ajax({
        url : callAddress,
        type : "GET",
        // handle a successful response
        success : function(newCode) {
        	$('.mainTable').remove();
        	$( ".searchBox" ).after(newCode);
        	activateRowSelection();
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("ERROR: "+errmsg)
        }
    });
}
function clearSelection(){
	$(".mainTableRow").each(function( index ) {
		if( $(this).hasClass('shaded')){
			$(this).css({"background-color":"#efefef"});
		}
		else{
			$(this).css({"background-color":"#fff"});
		}
		$(this).data("selected",false);
	});
}

function prepareDialogBoxes(){
	$('#tagTF').keypress(function(event){
	    if(event.keyCode == 13){
	    	event.preventDefault();
	        $("#tagButton").click();
	    }
	    else if(event.keyCode == 27){
	    	event.preventDefault();
	        $("#cancel1").click();
	    }
	});
	$('#untagTF').keypress(function(event){
	    if(event.keyCode == 13){
	    	event.preventDefault();
	        $("#untagButton").click();
	    }
	    else if(event.keyCode == 27){
	    	event.preventDefault();
	        $("#cancel2").click();
	    }
	});
	$('#addExpTF').keypress(function(event){
	    if(event.keyCode == 13){
	    	event.preventDefault();
	        $("#addExpButton").click();
	    }
	    else if(event.keyCode == 27){
	    	event.preventDefault();
	        $("#cancel4").click();
	    }
	});
	$('#removeExpTF').keypress(function(event){
	    if(event.keyCode == 13){
	    	event.preventDefault();
	        $("#removeExpButton").click();
	    }
	    else if(event.keyCode == 27){
	    	event.preventDefault();
	        $("#cancel3").click();
	    }
	});
}

////////////The buffer panel///////////////
function addSearchResultsToBP(){
	var currentURL = document.URL;
	var theData = currentURL.replace(/.*\?/,"");	//Because the query part starts with a "?"
	$.ajax({
        url : "../get-all-ids/",
        type : "GET", // http method
        data : theData, 
        // handle a successful response
        success : function(ids) {
        	var newListItem = $("<option class='lbo'></option>");
			newListItem.text("Selection "+bpsc+" ("+JSON.parse(ids).length+")");
			newListItem.attr("value",bpsc);
			newListItem.data("ids",ids);
			$('#listBox').append(newListItem);
			bpsc += 1;
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("ERROR: "+errmsg)
            alert("Something went wrong!");
        }
    });
}
function removeSelected(){
	$('#listBox').find(":selected").remove();
}
function clearBuffer(){
	$('#listBox').empty();
}
function addToBuffer(){
	//This is the function called when user clicks on "add to buffer" in the right click menu
	//I could as well have called it something like "rgtClkMenuAddToBuffer" to stay more consistent
	var highlightedRows = [];
	$(".mainTableRow").each(function( index ) {
		if($(this).data("selected")==true){
			highlightedRows.push($(this).children().last().html());
		}
	});
	//Now the variable highlightedRows contains the IDs of the selected images.
	var newListItem = $("<option class='lbo'></option>");
	newListItem.text("Selection "+bpsc+" ("+highlightedRows.length+")");
	newListItem.attr("value",bpsc);
	newListItem.data("ids",highlightedRows);
	$('#listBox').append(newListItem);
	bpsc += 1;
	$('#rightClickMenu').css('visibility','hidden');
}
function downloadBufferImages(isWithTrace){
	pourBufferImagesInTheRightVariable();
	$('#theHiddenField').val(imagesToBeManipulated);
	showDownloadDialog();
	//TODO
}
function showDownloadDialog(){
	$('#fullScreen').css('visibility','visible');
	$('#downloadDialog').css('visibility','visible');
}

////////////The Menu///////////////
function showMenu(menuName){
	$('.dropdownMenu').css('visibility','hidden');
	var theMenuBox = $('#'+menuName+'Menu');
	var theMenuButton = $('#'+menuName+'MenuButton'); 
	var pos = theMenuButton.position();
	var top = pos.top+30;
	var left = pos.left+241; 
	theMenuBox.css('top',top+"px");
	theMenuBox.css('left',left+"px");
	theMenuBox.css('visibility','visible');
}














////Trevor's stuff:
function openImport() {
	if (document.location.hostname != "localhost"){
		alert("You do not have access to this function. This incident will be reported.")
	}
	else{
		console.log("import dialog opened");

		$('#importDialog').css('visibility', 'visible');
	}
	
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
function deleteItem() {
	var selection = document.getElementById("imageSequences");
	console.log( "item " + selection.options[ selection.selectedIndex ].value + " deleted");
}

function submitImport() {
	var serialized = $('#importDialogForm').serialize();
	serialized = serialized.replace("tracers=m","tracers=3");
    

    $.ajax({
        url : "../addfiles/",
        type : "GET", // http method
        data : serialized, 
        // handle a successful response
        success : function(newCode) {
        	console.log("successfully read")
        	alert("Success!")
        	
        	$( "#importDialog" ).css('visibility','hidden');
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("ERROR: "+errmsg)
            alert("failure:"+errmsg)

        }
    });
};

//////////////////////////////
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}






////////////DB Manipulation///////////////
function rgtClkMenuTag(){
	pourHighlightedImagesToTheRightVariable();
	$('#rightClickMenu').css('visibility','hidden');
	showTaggingDialog();
}
function rgtClkMenuUntag(){
	pourHighlightedImagesToTheRightVariable();
	$('#rightClickMenu').css('visibility','hidden');
	showUntaggingDialog();
}
function tagBuffer(){
	pourBufferImagesInTheRightVariable();
	showTaggingDialog();
	
}
function untagBuffer(){
	//The function that's called when the menu item for untagging the images in the buffer panel is clicked
	pourBufferImagesInTheRightVariable();
	showUntaggingDialog();	
}
function pourBufferImagesInTheRightVariable(){
	var hash = {};
	$('#listBox').children().each(function () {
   		for (var i=0;i<$(this).data('ids').length;i++){
   			var id = $(this).data('ids')[i];
   			hash[id]= true;
   		} 
	});
	var imageIDs = Object.keys(hash);
	imagesToBeManipulated = imageIDs;
}
function showTaggingDialog(){
	$('#fullScreen').css('visibility','visible');
	$('#taggingDialog').css('visibility','visible');
	$('#tagTF').focus();
}

function showUntaggingDialog(){
	$('#fullScreen').css('visibility','visible');
	$('#untaggingDialog').css('visibility','visible');
	$('#untagTF').focus();
}
function removeDialog(){
		$('#fullScreen').css('visibility','hidden');
		$('.dialogBox').css('visibility','hidden');
}
function tag(){
	
	$.ajax({
        url : "../tag/",
        type : "POST", // http method
        data : {imgs: imagesToBeManipulated, tagContent: $('#tagTF').val()},  
        // handle a successful response
        success : function(response) {
        	alert("Successfully tagged images!");
        	console.log(response);
        	reloadTable();
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
        	alert("Something went wrong!");
            console.log("ERROR: "+errmsg)
        }
    });
    removeDialog();
}
function untag(){
	
	$.ajax({
        url : "../untag/",
        type : "POST", // http method
        data : {imgs: imagesToBeManipulated, tagContent: $('#untagTF').val()},  
        // handle a successful response
        success : function(response) {
        	alert("Successfully removed "+response+" tags!");
        	console.log(response);
        	reloadTable();
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
        	alert("Something went wrong!");
            console.log("ERROR: "+errmsg)
        }
    });
    removeDialog();
}

function pourHighlightedImagesToTheRightVariable(){
	var selectedImages = [];
	$(".mainTableRow").each(function( index ) {
		if($(this).data("selected")==true){
			selectedImages.push($(this).children().last().html());
		}
	});
	//Now the variable selectedImages contains the IDs of the selected images.
	imagesToBeManipulated = selectedImages;
}

////THIS IS STUDPID BUT NOW I HAVE THE SAME FUNCTIONS FOR EXPERIMENTS INSTEAD OF TAGS
function rgtClkMenuAddExp(){
	pourHighlightedImagesToTheRightVariable();
	$('#rightClickMenu').css('visibility','hidden');
	showAddExpDialog();
}
function rgtClkMenuRemoveExp(){
	pourHighlightedImagesToTheRightVariable();
	$('#rightClickMenu').css('visibility','hidden');
	showRemoveExpDialog();
}
function addExpBuffer(){
	pourBufferImagesInTheRightVariable();
	showAddExpDialog();
	
}
function removeExpBuffer(){
	pourBufferImagesInTheRightVariable();
	showRemoveExpDialog();	
}
function showAddExpDialog(){
	$('#fullScreen').css('visibility','visible');
	$('#addExpDialog').css('visibility','visible');
	$('#addExpTF').focus();
}

function showRemoveExpDialog(){
	$('#fullScreen').css('visibility','visible');
	$('#removeExpDialog').css('visibility','visible');
	$('#removeExpTF').focus();
}
function addExp(){
	
	$.ajax({
        url : "../addexp/",
        type : "POST", // http method
        data : {imgs: imagesToBeManipulated, expContent: $('#addExpTF').val()},  
        // handle a successful response
        success : function(response) {
        	alert("Successfully added experiment to images!");
        	console.log(response);
        	reloadTable();
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
        	alert("Something went wrong!");
            console.log("ERROR: "+errmsg)
        }
    });
    removeDialog();
}
function removeExp(){
	
	$.ajax({
        url : "../removeexp/",
        type : "POST", // http method
        data : {imgs: imagesToBeManipulated, expContent: $('#removeExpTF').val()},  
        // handle a successful response
        success : function(response) {
        	alert("Successfully removed "+response+" experiment tags!");
        	console.log(response);
        	reloadTable();
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
        	alert("Something went wrong!");
            console.log("ERROR: "+errmsg)
        }
    });
    removeDialog();
}