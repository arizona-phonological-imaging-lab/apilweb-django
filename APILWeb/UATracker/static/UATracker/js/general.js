var beginID;
var endID;
var selecting;
var bpsc = 1; //Buffer Panel Selection Counter
var imagesToBeManipulated = [];
var importType = 1;

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
	
	$(document).ajaxStart(function(){
	    $("input").prop("disabled", true);
	    $("button").prop("disabled", true);
	    $("#waitingImage").css("visibility", 'visible');
	});

	$(document).ajaxComplete(function(){
		$("input").prop("disabled", false);
		$("button").prop("disabled", false);
		$("#waitingImage").css("visibility", 'hidden');
	});

	if (document.location.hostname != "localhost" && document.location.hostname != "127.0.0.1"){
		$('#dataMenuButton').css('visibility','hidden');
	}
	
	
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
	console.log(imagesToBeManipulated)
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

