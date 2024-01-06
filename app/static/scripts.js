const selectAll = document.querySelector("#selectAll");

selectAll.addEventListener("click", () => {
  const table_checkboxes = document.querySelectorAll(
    'table tbody input[type="checkbox"]'
  );

  table_checkboxes.forEach((elm) => {
    elm.checked = selectAll.checked;
  });
});

// $(document).ready(function () {
//   // Activate tooltip
//   $('[data-bs-toggle="tooltip"]').tooltip();

//   $(".edit").on("click", function () {
//     var row = $(this).closest("tr");
//     var roomId = row.find("td:eq(1)").text();
//     var roomName = row.find("td:eq(2)").text();
//     var roomDescription = row.find("td:eq(3)").text();
//     var roomEnabled = row.find("td:eq(4)").text();
//     var roomStartDate = row.find("td:eq(5)").text();
//     var roomEndDate = row.find("td:eq(6)").text();

//     $("#editRoomId").val(roomId);
//     $("#editRoomName").val(roomName);
//     $("#editRoomDescription").val(roomDescription);
//     $("#editRoomEnabled").val(roomEnabled);
//     $("#editRoomStartDate").val(roomStartDate);
//     $("#editRoomEndDate").val(roomEndDate);
//   });

//   $(".delete").on("click", function () {
//     // Retrieve values from the selected row
//     var row = $(this).closest("tr");
//     var roomId = row.find("td:eq(1)").text();
//     console.log(roomId);
//   });

//   $("#addRoomForm").on("submit", function (event) {
//     event.preventDefault();
//     var formData = {
//       name: $("#addRoomName").val(),
//       description: $("addRoomDescription").val(),
//       enabled: $("#addRoomEnabled").val(),
//       start_date: new Date($("#addRoomStartDate").val()),
//       end_date: new Date($("#addRoomEndDate").val()),
//     };

//     console.log(formData);

//     $.ajax({
//       type: "POST",
//       url: "http://localhost:5000/api/v1/rooms",
//       data: formData,
//       dataType: "json",
//       encode: true,
//     }).done(function (data) {
//       console.log(data);
//     });

//     console.log(formData);
//   });
// });
