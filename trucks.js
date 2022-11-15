const BASE_URL = 'https://hidden-meadow-42569.herokuapp.com';

function loadTrucksFromServer() {
    var requestOptions = {
        credentials: "include"
    }
    fetch(`${BASE_URL}/trucks`, requestOptions).then((response) => {
        response.json().then((data) => {
            if (response.status == 200) {
                document.getElementById("logout").style.display = "block";
                console.log(data);
                var trucks = data.mytrucks;
                var meta = data.metadata;

                var container = document.getElementById("your_past_entries");
                container.innerHTML = "";

                trucks.forEach(function (truck) {
                    for ([key, value] of Object.entries(meta)) {
                        if (value.id == truck.name) {
                            var truckIndex = key;
                            truck.name = value.name;
                        }
                    }
    
                    var newItem = document.createElement("div");
                    newItem.classList.add("card");
                    for ([key, attr] of Object.entries(truck)) {
                        user = truck.user_id;
                        if (key == 'id') {
                            newItem.innerHTML += `<img src='./truck_icons/${meta[truckIndex].slug}.png' alt='truck icon' class='truck_icon'/>`;
                            newItem.innerHTML += `<p class="truck_cuisine">${meta[truckIndex].cuisine}</p>`;
                        } else if (key == 'type' || key == 'review') {
                            str = attr.substring(0, 27);
                            if (str.length >= 27) {
                                str += "...";
                            }
                            newItem.innerHTML += `<p><strong>${key.toUpperCase()}:</strong> ${str}</p>`;
                        } else if (key == "user_id") {
                            newItem.innerHTML += `<p><strong>POSTED BY:</strong> ${user}</p>`;
                        } else {
                            newItem.innerHTML += `<p><strong>${key.toUpperCase()}:</strong> ${attr}</p>`;
                        }
                    }
                    container.appendChild(newItem);
                });

                displayContent();
            }
            loadYourTrucksFromServer();
            return response.status;
        })
        .catch((error) => {
            console.log("ERROR:", error, response.status);
        });
    });
}

function loadYourTrucksFromServer() {
    var requestOptions = {
        credentials: "include"
    }
    fetch(`${BASE_URL}/trucks?user=True`, requestOptions).then((response) => {
        response.json().then((data) => {
            if (response.status == 200) {
                var trucks = data.mytrucks;
                var meta = data.metadata;

                var yourContainer = document.getElementById("past_entries");
                yourContainer.innerHTML = "";

                trucks.forEach(function (truck) {
                    for ([key, value] of Object.entries(meta)) {
                        if (value.id == truck.name) {
                            var truckIndex = key;
                            truck.name = value.name;
                        }
                    }
    
                    var yourItem = document.createElement("div");
                    yourItem.setAttribute("onclick", `loadSingleTruckFromServer('${truck.id}')`);
                    yourItem.classList.add("card");
                    for ([key, attr] of Object.entries(truck)) {
                        if (key == 'id') {
                            yourItem.innerHTML += `<img src='./truck_icons/${meta[truckIndex].slug}.png' alt='truck icon' class='truck_icon'/>`;
                            yourItem.innerHTML += `<p class="truck_cuisine">${meta[truckIndex].cuisine}</p>`;
                        } else if (key == 'type' || key == 'review') {
                            str = attr.substring(0, 27);
                            if (str.length >= 27) {
                                str += "...";
                            }
                            yourItem.innerHTML += `<p><strong>${key.toUpperCase()}:</strong> ${str}</p>`;
                        } else if (key != "user_id") {
                            yourItem.innerHTML += `<p><strong>${key.toUpperCase()}:</strong> ${attr}</p>`;
                        }
                    }
                    yourItem.innerHTML += `<div class="edit_btn_underlay"></div><div class="btn" id="edit_btn">Edit Review</div>`;
                    yourContainer.appendChild(yourItem);
                });

                displayContent();
            }
            return response.status;
        })
        .catch((error) => {
            console.log("ERROR:", error, response.status);
        });
    });
}

function loadSingleTruckFromServer(id) {
    var requestOptions = {
        credentials: "include"
    }
    fetch(`${BASE_URL}/trucks/${id}`, requestOptions).then((response) => {
        response.json().then((data) => {
            if (response.status == 200) {
            truck = data.mytruck;
            meta = data.metadata;
            for ([key, value] of Object.entries(meta)) {
                if (value.id == truck.name) {
                    truck.name = value.name;
                }
            }
            var container = document.getElementById("modal");
            container.style.display = "block";
            document.getElementById("modal_underlay").style.display = "block";

            var form = document.querySelector("#edit_form");
            form.querySelector("#name").value = truck.name;
            form.querySelector("#type").value = truck.type;
            form.querySelector("#rating").value = truck.rating;
            form.querySelector("#review").value = truck.review;
            form.querySelector("#location").value = truck.location;

            container.querySelector("#delete_truck_btn").onclick = function () {
                deleteSingleTruck(truck.id);
            }

            container.querySelector("#edit_truck_btn").onclick = function () {
                var name = form.querySelector("#name").value;
                var type = form.querySelector("#type").value;
                var rating = form.querySelector("#rating").value;
                var review = form.querySelector("#review").value;
                var location = form.querySelector("#location").value;
                editSingleTruck(truck.id, name, type, rating, review, location);
            }
        }})
        .catch((error) => {
            console.log("ERROR:", error, response.status);
        });
    });
}

function deleteSingleTruck(id) {
    if (confirm("Are you sure you want to delete this truck review?")) {
        closeModal();
        var requestOptions = {
            method: "DELETE",
            credentials: "include"
        }
        fetch(`${BASE_URL}/trucks/${id}`, requestOptions).then((response) => {
            loadTrucksFromServer();
        });
    }
}

function editSingleTruck(id, name, type, rating, review, location) {
    closeModal();
    var data = [`name=${encodeURIComponent(name)}&type=${encodeURIComponent(type)}&rating=${encodeURIComponent(rating)}&review=${encodeURIComponent(review)}&location=${encodeURIComponent(location)}`];
    var requestOptions = {
        method: "PUT",
        body: data,
        credentials: "include",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
    }
    fetch(`${BASE_URL}/trucks/${id}`, requestOptions).then((response) => {
        loadTrucksFromServer();
    });
}

document.getElementById("submit_btn").onclick = function () {
    var name = document.querySelector("#name").value;
    var type = document.querySelector("#type").value;
    var rating = document.querySelector("#rating").value;
    var review = document.querySelector("#review").value;
    var location = document.querySelector("#location").value;
    createTruckOnServer(name, type, rating, review, location);
}

function closeModal() {
    document.getElementById("modal").style.display = "none";
    document.getElementById("modal_underlay").style.display = "none";
}

document.getElementById("close_modal").onclick = closeModal;
document.getElementById("modal_underlay").onclick = closeModal;

function createTruckOnServer(name, type, rating, review, location) {
    var data = [`name=${encodeURIComponent(name)}&type=${encodeURIComponent(type)}&rating=${encodeURIComponent(rating)}&review=${encodeURIComponent(review)}&location=${encodeURIComponent(location)}`];
    var requestOptions = {
        method: "POST",
        body: data,
        credentials: "include",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
    }
    fetch(`${BASE_URL}/trucks`, requestOptions).then((response) => {
        loadTrucksFromServer();
        document.querySelector("#name").value = '';
        document.querySelector("#type").value = '';
        document.querySelector("#review").value = '';
        document.querySelector("#rating").value = '';
        document.querySelector("#location").value = '';
    }).catch((error) => {
        console.log(error);
    });
}

function displayContent() {
    document.getElementById("main_form").style.display = "block";
    document.getElementById("responses").style.display = "block";
    document.getElementById("login_form").style.display = "none";
    document.getElementById("signup_form").style.display = "none";
}

loadTrucksFromServer();