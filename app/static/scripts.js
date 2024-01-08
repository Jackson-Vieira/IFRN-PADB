const API_V1_URL = "http://localhost:5000/api/v1";

const selectAll = document.querySelector("#selectAll");
const searchInput = document.querySelector("#search");
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

if (document.querySelector(".edit")) {
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
}

if (document.querySelector(".delete")) {
  document.querySelector(".delete").addEventListener("click", function (event) {
    const row = this.closest("tr");
    const roomId = row.querySelectorAll("td")[1].textContent;
    console.log("Deleted Room ID", roomId);
    deleteRoomForm.id.value = roomId;
  });
}

function getFormValues(form) {
  const formData = new FormData(form);
  const values = {};
  formData.forEach((value, key) => {
    if (value !== "" && value !== undefined) {
      values[key] = value;
    }
  });
  return values;
}

async function postData(url, data) {
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    return response;
  } catch (error) {
    console.error("Error:", error);
  }
}

async function putData(url, data) {
  try {
    const response = await fetch(url, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    return response;
  } catch (error) {
    console.error("Error:", error);
  }
}

async function deleteData(url) {
  try {
    const response = await fetch(url, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    });
    return response;
  } catch (error) {
    console.error("Error:", error);
  }
}

addRoomForm.addEventListener("submit", async function (event) {
  event.preventDefault();
  const formData = getFormValues(this);
  const url = API_V1_URL + "/rooms";

  const response = await postData(url, formData);
});

editRoomForm.addEventListener("submit", async function (event) {
  event.preventDefault();
  const formData = getFormValues(this);
  const url = API_V1_URL + "/rooms/" + formData.id;

  const response = await putData(url, formData);
});

deleteRoomForm.addEventListener("submit", async function (event) {
  event.preventDefault();
  const roomId = deleteRoomForm.id.value;
  const url = API_V1_URL + "/rooms/" + roomId;

  const response = await deleteData(url);
});

function handleSearchFilterRoom(event) {
  let input = searchInput.value;
  // TODO: make request and update rooms table
}

function handleClickEditRoom(event) {
  console.log(event);
  // TODO: handle this
}

function handleClickDeleteRoom(event) {
  console.log(event);
  // TODO: handle this
}
