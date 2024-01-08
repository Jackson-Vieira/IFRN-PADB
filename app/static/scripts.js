const API_V1_URL = "http://localhost:5000/api/v1";

const searchInput = document.querySelector("#searchInput");
const addRoomForm = document.forms["addRoomForm"];
const editRoomForm = document.forms["editRoomForm"];
const deleteRoomForm = document.forms["deleteRoomForm"];

// -- Bootstrap --

const deleteRoomModal = new bootstrap.Modal(
  document.getElementById("deleteRoomModal"),
  {
    keyboard: false,
  }
);

const addRoomModal = new bootstrap.Modal(
  document.getElementById("addRoomModal"),
  {
    keyboard: false,
  }
);

const editRoomModal = new bootstrap.Modal(
  document.getElementById("editRoomModal"),
  {
    keyboard: false,
  }
);

// -- END Bootstrap --

function addRoomRowToTable(roomData) {
  const table = document
    .getElementById("roomsTable")
    .getElementsByTagName("tbody")[0];

  const row = document.createElement("tr");

  const rowData = `
        ${roomData
          .map(
            (data) =>
              `<td${data === true ? ' class="active"' : ""}>${data}</td>`
          )
          .join("")}
        <td>
            <a data-bs-target="#editRoomModal" class="edit" data-bs-toggle="modal" onclick="handleClickEditRoom(event)">
							<svg class="w-[24px] h-[24px] text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 18">
    							<path d="M12.687 14.408a3.01 3.01 0 0 1-1.533.821l-3.566.713a3 3 0 0 1-3.53-3.53l.713-3.566a3.01 3.01 0 0 1 .821-1.533L10.905 2H2.167A2.169 2.169 0 0 0 0 4.167v11.666A2.169 2.169 0 0 0 2.167 18h11.666A2.169 2.169 0 0 0 16 15.833V11.1l-3.313 3.308Zm5.53-9.065.546-.546a2.518 2.518 0 0 0 0-3.56 2.576 2.576 0 0 0-3.559 0l-.547.547 3.56 3.56Z"/>
    							<path d="M13.243 3.2 7.359 9.081a.5.5 0 0 0-.136.256L6.51 12.9a.5.5 0 0 0 .59.59l3.566-.713a.5.5 0 0 0 .255-.136L16.8 6.757 13.243 3.2Z"/>
  							</svg>
						</a>
            <a data-bs-target="#deleteRoomModal" class="delete" data-bs-toggle="modal" onclick="handleClickDeleteRoom(event)">
							<svg class="w-[24px] h-[24px] text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 18 20">
    							<path d="M17 4h-4V2a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2v2H1a1 1 0 0 0 0 2h1v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V6h1a1 1 0 1 0 0-2ZM7 2h4v2H7V2Zm1 14a1 1 0 1 1-2 0V8a1 1 0 0 1 2 0v8Zm4 0a1 1 0 0 1-2 0V8a1 1 0 0 1 2 0v8Z"/>
  							</svg>
						</a>  
        </td>
    `;

  row.innerHTML = rowData;
  table.appendChild(row);
}

function updateRoomsTable(roomsArray) {
  const table = document
    .getElementById("roomsTable")
    .getElementsByTagName("tbody")[0];

  table.innerHTML = "";

  roomsArray.forEach((room) => {
    addRoomRowToTable(room);
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

async function getData(url) {
  try {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    return await response.json();
  } catch (error) {
    console.error("Error:", error);
  }
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
  addRoomModal.toggle();
  getRooms();
});

editRoomForm.addEventListener("submit", async function (event) {
  event.preventDefault();
  const formData = getFormValues(this);
  const url = API_V1_URL + "/rooms/" + formData.id;
  const response = await putData(url, formData);
  editRoomModal.toggle();
  getRooms();
});

deleteRoomForm.addEventListener("submit", async function (event) {
  event.preventDefault();
  const roomId = deleteRoomForm.id.value;
  const url = API_V1_URL + "/rooms/" + roomId;
  const response = await deleteData(url);
  deleteRoomModal.toggle();
  getRooms();
});

function debounce(func, delay) {
  let timer;
  return function () {
    const context = this;
    const args = arguments;
    clearTimeout(timer);
    timer = setTimeout(() => {
      func.apply(context, args);
    }, delay);
  };
}

async function getRooms(params) {
  const url = API_V1_URL + "/rooms";

  if (params) url = url + "?search=" + params;

  const response = await getData(url);
  updateRoomsTable(response.data);
}

searchInput.addEventListener(
  "keyup",
  debounce(async function () {
    const searchText = searchInput.value;
    const url = API_V1_URL + "/rooms?search=" + searchText;
    const response = await getData(url);
    updateRoomsTable(response.data);
  }, 300)
);

function handleClickEditRoom(event) {
  const row = event.target.closest("tr");
  const [
    roomId,
    roomName,
    roomDescription,
    roomEnable,
    roomStartDate,
    roomEndDate,
  ] = Array.from(row.querySelectorAll("td")).map((td) => td.textContent);

  document.querySelector("#editRoomId").value = roomId;
  document.querySelector("#editRoomName").value = roomName;
  document.querySelector("#editRoomDescription").value = roomDescription;
  document.querySelector("#editRoomEnabled").value = roomEnable === "True";
  document.querySelector("#editRoomStartDate").value = roomStartDate;
  document.querySelector("#editRoomEndDate").value = roomEndDate;
}

function handleClickDeleteRoom(event) {
  const row = event.target.closest("tr");
  const roomId = row.querySelectorAll("td")[0].textContent;
  deleteRoomForm.id.value = roomId;
}
