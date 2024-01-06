const selectAll = document.querySelector("#selectAll");

// forms
const addRoomForm = document.forms["addRoomForm"];
const editRoomForm = document.forms["editRoomForm"];
const deleteRoomForm = document.forms["deleteRoomForm"];

selectAll.addEventListener("click", () => {
  const table_checkboxes = document.querySelectorAll(
    'table tbody input[type="checkbox"]'
  );

  table_checkboxes.forEach((elm) => {
    elm.checked = selectAll.checked;
  });
});

document.querySelector(".edit").addEventListener("click", (event) => {
  const row = event.target.closest("tr");
  const [
    roomId,
    roomName,
    roomDescription,
    roomEnable,
    roomStartDate,
    roomEndDate,
  ] = Array.from(row.querySelectorAll("td"))
    .slice(1)
    .map((td) => td.textContent);

  document.querySelector("#editRoomId").value = roomId;
  document.querySelector("#editRoomName").value = roomName;
  document.querySelector("#editRoomDescription").value = roomDescription;
  document.querySelector("#editRoomEnabled").value = roomEnable === "True";
  document.querySelector("#editRoomStartDate").value = roomStartDate;
  document.querySelector("#editRoomEndDate").value = roomEndDate;
});

document.querySelector(".delete").addEventListener("click", function (event) {
  const row = this.closest("tr");
  const roomId = row.querySelectorAll("td")[1].textContent;
  console.log("Deleted Room ID", roomId);
  deleteRoomForm.id.value = roomId;
});

function getValues(form) {
  return {
    id: form.id.value,
    name: form.name.value,
    description: form.description.value,
    enabled: form["enabled"].value,
    start_date: form.start_date.value,
    room_end_data: form.end_date.value,
  };
}

addRoomForm.addEventListener("submit", function (event) {
  event.preventDefault();
  let formData = getValues(this);
  console.log(formData);
});

editRoomForm.addEventListener("submit", function (event) {
  event.preventDefault();
  let formData = getValues(this);
  console.log(formData);
});

deleteRoomForm.addEventListener("submit", function (event) {
  event.preventDefault();
  const roomId = deleteRoomForm.id.value;
  console.log("Delete room with the id:", roomId);
});
