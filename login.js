const API_URL = 'http://127.0.0.1:8001';

async function Login(){
    try{
        username = document.getElementById("log-username").value;
        console.log("username: ",username);
        password = document.getElementById("log-password").value;
        console.log("password: ",password)
        response = await fetch(API_URL+`/login/?username=${username}&password=${password}`)
        console.log("response recieved:",response)
        if (! response.ok){
            throw new Error(`HTTP error! status: ${response.status}`)
        }
        res = await response.json();
        console.log(res)
        if (res["logged in"] == true){
            localStorage.setItem("AdaptToken",res["token"])
            window.location.replace("./index.html")
        }
    }
    catch (error) {
        // Fixed error handling
        console.error("Error occurred:", error.message);
        console.error("Full error:", error);
        alert("Login error: " + error.message);
        return null;
    }
}

async function Register(){
    username = document.getElementById("reg-username").value;
    email = document.getElementById("reg-email").value;
    password = document.getElementById("reg-password").value;
    repassword = document.getElementById("reg-repassword").value;
    try{
        response = await fetch(`${API_URL}/register`,{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password,
                api_key:"1"
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Registration failed');
        }
        setTimeout(() => {
            window.location.href = 'login.html';
        }, 2000);
    }
    catch (error){
        console.error('Registration error:', error);
        return { success: false, error: error.message };
    }
}

function show_msg(details, type='info'){
    box=document.getElementById("msg")
    box.textContent = details;
    box.className = `msg show ${type}`;
}

function hideMessage() {
    const box = document.getElementById('msg');
    if (box) {
        box.className = 'msg';
    }
}




