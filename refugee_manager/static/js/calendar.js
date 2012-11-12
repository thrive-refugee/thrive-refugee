function calendarLoad(){
	try{
	$(document).ready(function() {	
		var date = new Date();
		var d = date.getDate();
		var m = date.getMonth();
		var y = date.getFullYear();		
	
		$('#calendar').fullCalendar({
			header: {
				left: 'prev,next today',
				center: 'title',
				right: 'month,basicWeek,basicDay'
			},
			editable: false,
			events: $.getJSON('/refugee_manager/events'),
    		eventClick: function(event, element) {
				<!-- Event Infomation Fields -->
				$('#contactName').val(event.contactName);
				$('#contactPhone').val(event.contactPhone);
				$('#contactAddress').val(event.contactAddress);
				$('#contactEmail').val(event.contactEmail);
				$('#contactNotes').text(event.contactNotes);

				<!-- Event Control Fields -->
				var isAllDay = document.getElementById('eventIsAllDay').checked;				
				$('#eventTitle').val(event.title);
				$('#eventStartDate').val(event.start);
				$('#eventEndDate').val(event.end);
				$('#eventURL').val(event.url);
				$('#eventIsAllDay').val( (isAllDay) );
				var color = $('#eventColor').val();
				var backgroundColor = $('#eventBackgroundColor').val();
				var textColor = $('#eventTextColor').val();
				
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
	});
	} catch(exception){
		console.log("Unable to load the calendar!\nError Message:\n" + exception.description);
	}
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
