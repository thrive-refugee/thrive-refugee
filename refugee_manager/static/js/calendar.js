function calendarLoad(){
    var date = new Date(), d = date.getDate(), m = date.getMonth(), y = date.getFullYear();
    try{
	$('#calendar').fullCalendar({
	    header: {
		left: 'prev,next today',
		center: 'title',
		right: 'month,basicWeek,basicDay'
	    },
	    editable: false,
	    events: {
		url: '/refugee_manager/events',
		success: function(data) {
		    // take our data and make it into a format that fc likes
		    var fcData = [];
		    if (( data ) && ( data.length )) {
			$.each(data, function(index, item) {
			    fcData.push(makeFCEvent(item));
			});
		    }
		    return fcData;
		},
		error: function() {
		    alert("Error while fetching events");
		},
		color: 'blue',
		textColor: 'black'
	    },
    	    eventClick: function(event, jsEvent, view) {
		var isAllDay, color, backgroundColor, textColor;
		$('#contactName').val(event.contactName);
		$('#contactPhone').val(event.contactPhone);
		$('#contactAddress').val(event.contactAddress);
		$('#contactEmail').val(event.contactEmail);
		$('#contactNotes').text(event.contactNotes);
		
		isAllDay = document.getElementById('eventIsAllDay').checked;
		$('#eventTitle').val(event.title);
		$('#eventStartDate').val(event.start);
		$('#eventEndDate').val(event.end);
		$('#eventURL').val(event.url);
		$('#eventIsAllDay').val( isAllDay );
		color = $('#eventColor').val();
		backgroundColor = $('#eventBackgroundColor').val();
		textColor = $('#eventTextColor').val();
				
		if(color == null || color == ""){
		    color = '#FFFFFF';
		} else if(color.charAt(0) != '#') {
		    color = '#' + color;
		}
		    
		if(backgroundColor == null || backgroundColor == ""){
		    backgroundColor = '#FFFFFF';
		} else if(backgroundColor.charAt(0) != '#') {
		    backgroundColor = '#' + backgroundColor;
		}
		    
		if(textColor == null || textColor == ""){
		    textColor = '#FFFFFF';
		} else if(textColor.charAt(0) != '#') {
		    textColor = '#' + textColor;
		}
		    
		$('#eventColor').val(color);
		$('#eventBackgroundColor').val(backgroundColor);
		$('#eventTextColor').val(textColor);	
   	    }
	});
    } catch(exception){
	console.log("Unable to load the calendar!\nError Message:\n" + exception.description);
    }
}

function makeFCEvent(item) {
    var fcItem = item.fields;
    fcItem.id = item.pk;
    fcItem.model = item.model;
    return fcItem;
}

function makeDjangoEvent(item) {
    var tmp = $.extend({}, item); // leave original alone
    delete tmp.id;
    delete tmp.model;
    return ({
	pk: item.id,
	model: item.model,
	fields: tmp
    });
}

function appendCalendarEvent(){
    // TODO: Validation
    var eventObject = EventObject();
    
    $.ajax({
	url: '',
	data: eventObject.toJSON(),
	type: 'POST',
	dataType: 'json',
	cache: false,
	success: function(){
	    alert("Success!\nCalendar was updated.");		
	},
	failure: function(){
	    alert("Failure!\nCalendar wasn't updated, please try again.");
	}
    });

// TODO: clear textboxs
// TODO: Full page refresh!
}

function deleteCalendarEvent(){
    var eventObject = EventObject();
    
    // Ajax call, unsure if post or put
    $.ajax({
	url: '/refugee_manager/events',
	data: eventObject.toJSON(),
	type: 'DELETE',
	dataType: 'json',
	cache: false,
	success: function(){
	    alert("Success!\nCalendar event was deleted.");		
	},
	failure: function(){
	    alert("Failure!\nCalendar event wasn't deleted, please try again.");
		}
    });
}

function EventObject(){
    var that = {};
    that.eventId = ($('#eventId').val() == null) ? "" : $('#eventId').val();
    that.eventTitle = ($('#eventTitle').val() == null) ? "" : $('#eventTitle').val();
    that.eventStartDate = ($('#eventStartDate').val() == null) ? "" : $('#eventStartDate').val();
    that.eventEndDate = ($('#eventEndDate').val() == null) ? "" : $('#eventEndDate').val();
    that.eventURL = ($('#eventURL').val() == null) ? "" : $('#eventURL').val();
    that.eventIsAllDay = ($('#eventIsAllDay').val() == null) ? "" : $('#eventIsAllDay').val();
    that.eventColor = ($('#eventColor').val() == null) ? "#FFFFFF" : $('#eventColor').val();
    that.eventBackgroundColor = ($('#eventBackgroundColor').val() == null) ? "#FFFFFF" : $('#eventBackgroundColor').val();
    that.eventTextColor = ($('#eventTextColor').val() == null) ? "#FFFFFF" : $('#eventTextColor').val();
    that.contactName = ($('#contactName').val() == null) ? "" : $('#contactName').val();
    that.contactAddress = ($('#contactAddress').val() == null) ? "" : $('#contactAddress').val();
    that.contactPhone = ($('#contactPhone').val() == null) ? "" : $('#contactPhone').val();
    that.contactEmail = ($('#contactEmail').val() == null) ? "" : $('#contactEmail').val();
    that.contactNotes = ($('#contactNotes').text() == null) ? "" : $('#contactNotes').text();
    
    // Lazy hack, would freeze when to convert object to json
    that.toJSON = function(){
	return "{id:" + that.eventId + ", title:"+that.eventTitle + ", start:" + that.eventStartDate + ", end:" + that.eventEndDate +", url: " + that.eventURL + ", allDay:" + that.eventIsAllDay + ", color:" + that.eventColor + ", backgroundColor:"+ that.eventBackgroundColor + ", textColor: " + that.eventTextColor + ", contactName:" + that.contactName + ", contactAddress:" + that.contactAddress + ", contactPhone: " + that.contactPhone + ", contactEmail: " + that.contactEmail + ", contactNotes: " + that.contactNotes +" }" };

    return that;
}
