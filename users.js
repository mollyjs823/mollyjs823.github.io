const BASE_URL = 'https://hidden-meadow-42569.herokuapp.com';

function toggleLogin() {
    var logIn = document.getElementById("login_form");
    var signUp = document.getElementById("signup_form");
    console.log(logIn.style.display, signUp.style.display);
    if (signUp.style.display == 'none') {
        logIn.style.display = 'none';
        signUp.style.display = 'grid';
    } else {
        logIn.style.display = 'grid';
        signUp.style.display = 'none';
    }
}

for (btn of document.querySelectorAll(".switch_login")) {
    btn.onclick = toggleLogin;
}


function logoutUser() {
    var requestOptions = {
        method: "POST",
        credentials: "include",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
    }
    fetch(`${BASE_URL}/logout`, requestOptions).then((response) => {
        if (response.status == 201) {
            location.reload();
        } else {
            usrMsg.querySelector("#msg_content").innerHTML = "Unable to log out at this time :(";
            usrMsg.style.display = "flex";
            usrMsg.style.backgroundColor = "#d41746";
        }
    });
}
document.getElementById("logout").onclick = logoutUser;


var usrMsg = document.querySelector("#usr_msg");

document.getElementById("signin_btn").onclick = function () {
    var email = document.querySelector("#email").value;
    var fname = document.querySelector("#fname").value;
    var lname = document.querySelector("#lname").value;
    var password = document.querySelector("#password").value;
    createUserOnServer(email, fname, lname, password);
}

document.getElementById("login_btn").onclick = function () {
    var email = document.querySelector("#email_login").value;
    var password = document.querySelector("#password_login").value;
    login(email, password);
}

function login(email, password) {
    var data = [`email=${encodeURIComponent(email)}&password=${password}`];
    var requestOptions = {
        method: "POST",
        body: data,
        credentials: "include",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
    }
    fetch(`${BASE_URL}/sessions`, requestOptions).then((response) => {
        document.querySelector("#email_login").value = '';
        document.querySelector("#password_login").value = '';
        if (response.status == 201) {
            usrMsg.querySelector("#msg_content").innerHTML = "You are now logged in!";
            usrMsg.style.display = "flex";
            usrMsg.style.backgroundColor = "#00ffae";
            console.log(response.text);
            loadTrucksFromServer();
        } else {
            usrMsg.querySelector("#msg_content").innerHTML = "You entered the wrong email or password :(";
            usrMsg.style.display = "flex";
            usrMsg.style.backgroundColor = "#d41746";
        }
    });
}

function createUserOnServer(email, fname, lname, password) {
    var data = [`email=${encodeURIComponent(email)}&fname=${encodeURIComponent(fname)}&lname=${encodeURIComponent(lname)}&password=${encodeURIComponent(password)}`];
    var requestOptions = {
        method: "POST",
        body: data,
        credentials: "include",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
    }
    fetch(`${BASE_URL}/users`, requestOptions).then((response) => {
        if (response.status == 201) {
            document.querySelector("#email").value = '';
            document.querySelector("#fname").value = '';
            document.querySelector("#password").value = '';
            document.querySelector("#lname").value = '';
            usrMsg.querySelector("#msg_content").innerHTML = "Your account was created successfully!";
            usrMsg.style.display = "flex";
            usrMsg.style.backgroundColor = "#00ffae";
            console.log("Loading");
            login(email, password);
        } else {
            usrMsg.querySelector("#msg_content").innerHTML = "This account already exists :(";
            usrMsg.style.display = "flex";
            usrMsg.style.backgroundColor = "#d41746";
        }
    });
}

function closeMessage() {
    usrMsg.style.display = "none";
}

document.getElementById("close_btn").onclick = closeMessage;
