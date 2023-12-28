$(document).ready(function(){
	// Activate tooltip
	$('[data-bs-toggle="tooltip"]').tooltip();
	
	// Select/Deselect checkboxes
	const checkbox = $('table tbody input[type="checkbox"]');
	$("#selectAll").click(function(){
		if(this.checked){
			checkbox.each(function(){
				this.checked = true;                        
			});
		} else{
			checkbox.each(function(){
				this.checked = false;                        
			});
		} 
	});
	checkbox.click(function(){
		if(!this.checked){
			$("#selectAll").prop("checked", false);
		}
	});

	$('.edit').on('click', function () {
        var row = $(this).closest('tr');
        var roomId = row.find('td:eq(1)').text();
        var roomName = row.find('td:eq(2)').text();
        var roomDescription = row.find('td:eq(3)').text();
        var roomEnabled = row.find('td:eq(4)').text();
        var roomStartDate = row.find('td:eq(5)').text();
        var roomEndDate = row.find('td:eq(6)').text();

        $('#editRoomId').val(roomId);
        $('#editRoomName').val(roomName);
        $('#editRoomDescription').val(roomDescription);
        $('#editRoomEnabled').val(roomEnabled);
        $('#editRoomStartDate').val(roomStartDate);
        $('#editRoomEndDate').val(roomEndDate);
    });


	$('.delete').on('click', function () {
		// Retrieve values from the selected row
		var row = $(this).closest('tr');
		var roomId = row.find('td:eq(1)').text();
		console.log(roomId);
	});

	$('#addRoomForm').on('submit', function(event){
		event.preventDefault();
	});
});