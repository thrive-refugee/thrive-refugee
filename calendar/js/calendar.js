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
			events: [
				{
					id: 0000,
					title: 'Bit Diddler Activity Work',
					start: new Date(y, m, d-3, 16, 0),
					color: '#5CFF87',
					allDay: true,
					contactName: 'Bit Diddler',
					contactPhone: '000-000-0000',
					contactAddress: 'Somewhere St.',
					contactEmail: 'bit@gmail.com',
					contactNotes: 'Bit Diddler is the man.'
					
				}, {
					id: 0001,
					title: 'Bob Activity Work',
					start: new Date(y, m, d+4, 16, 0),
					allDay: true,
					contactName: 'Bob',
					contactPhone: '111-111-1111',
					contactAddress: 'Somewhere St.',
					contactEmail: 'bob@gmail.com',
					contactNotes: 'Has trouble with females.'
				}
			],
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
				$('#eventColor').val( (event.color.charAt(0) != '#') ?  ('#' + event.color) : event.color);
				$('#eventBackgroundColor').val( (event.color.charAt(0) != '#') ?  ('#' + event.backgroundColor) : event.backgroundColor);
				$('#eventTextColor').val('#' + event.textColor);	
   			}
		});
	});
	} catch(exception){
		console.log("Unable to load the calendar!\nError Message:\n" + exception.description);
	}
}


function appendCalendarEvent(){
	// TODO: Validation!
	
	function EventObject(eventId, eventTitle, eventStartDate, eventEndDate, eventURL, eventIsAllDay, eventColor, eventTextColor, contactName, contactAddress, contactPhone, contactEmail, contactNotes){
		this.eventId = eventId;
		this.eventTitle = eventTitle;
		this.eventStartDate = eventStartDate;
		this.eventEndDate = eventEndDate;
		this.eventURL = eventURL;
		this.eventIsAllDay = eventIsAllDay;
		this.eventColor = eventColor;
		this.eventTextColor = eventTextColor;
		this.contactName = contactName;
		this.contactAddress = contactAddress;
		this.contactPhone = contactPhone;
		this.contactEmail = contactEmail;
		this.contactNotes = contactNotes;
		this.CRUD_CONTROL = "APPEND";
	}

	var JSONEvent = EventObject(
		$('#eventId').val(),
		$('#eventTitle').val(), 
		$('#eventStartDate').val(), 
		$('#eventEndDate').val(), 
		$('#eventURL').val(), 
		$('#eventIsAllDay').val(), 
		$('#eventColor').val(), 
		$('#eventBackgroundColor').val(),
		$('#eventTextColor').val(), 
		$('#contactName').val(),
		$('#contactAddress').val(),
		$('#contactPhone').val(),
		$('#contactEmail').val(),
		$('#contactNotes').text()
	)	

	// Ajax call, unsure if post or put
	$.ajax({
		url: '',
		data: Object.toJSON(JSONEvent),
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

function deleteEvent(){
	function EventObject(eventId, eventTitle, eventStartDate, eventEndDate, eventURL, eventIsAllDay, eventColor, eventTextColor, contactName, contactAddress, contactPhone, contactEmail, contactNotes){
		this.eventId = eventId;
		this.eventTitle = eventTitle;
		this.eventStartDate = eventStartDate;
		this.eventEndDate = eventEndDate;
		this.eventURL = eventURL;
		this.eventIsAllDay = eventIsAllDay;
		this.eventColor = eventColor;
		this.eventTextColor = eventTextColor;
		this.contactName = contactName;
		this.contactAddress = contactAddress;
		this.contactPhone = contactPhone;
		this.contactEmail = contactEmail;
		this.contactNotes = contactNotes;
		this.CRUD_CONTROL = "DELETE";
	}

	var JSONEvent = EventObject(
		$('#eventId').val(),
		$('#eventTitle').val(), 
		$('#eventStartDate').val(), 
		$('#eventEndDate').val(), 
		$('#eventURL').val(), 
		$('#eventIsAllDay').val(), 
		$('#eventColor').val(), 
		$('#eventBackgroundColor').val(),
		$('#eventTextColor').val(), 
		$('#contactName').val(),
		$('#contactAddress').val(),
		$('#contactPhone').val(),
		$('#contactEmail').val(),
		$('#contactNotes').text()
	)	

	// Ajax call, unsure if post or put
	$.ajax({
		url: '',
		data: Object.toJSON(JSONEvent),
		type: 'POST',
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
