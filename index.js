(
    function () {
        document.getElementById("btn").addEventListener("click", async () => {
            let email = document.getElementById("email").value
            let password = document.getElementById("password").value
            const body = {
                "email": email,
                "password": password
            }
            let data = await callApi(body, "http://localhost:8081/login")
            if (data["status"] == "success") {
                let userid = data["data"]
                console.log(userid);
                localStorage.setItem("userid", userid)
                location.href = location.origin + "/todo.html"
            } else {
                document.getElementById("alert").innerHTML = `<div class="w-4/12 bg-orange-800 m-auto my-4 p-0 rounded-2xl">
                <div class="my-4 py-1">
                    <span
                        class="mx-2 text-md bg-orange-500 rounded-2xl px-3 text-white my-2 hover:bg-orange-300 shadow-lg shadow-slate-900">
                        Warning
                    </span>
                    <span class="mx-2 text-lg font-semi-bold rounded-2xl px-3 text-white my-2">
                        Enter correct credentials
                    </span>
                </div>
            
            </div>`
                setTimeout(() => {
                    document.getElementById("alert").innerHTML = ''
                }, 3000)
            }

        })

        document.getElementById("signup").addEventListener("click", async () => {
            document.getElementById("name").classList.toggle("hidden")
            let btnElement = document.getElementById("btn")
            let switchElement = document.getElementById("signup")
            if (btnElement.innerText === "Sign in") {
                btnElement.innerText = "Sign up"
                switchElement.innerText = "Signin"
            } else {
                btnElement.innerText = "Sign in"
                switchElement.innerText = "Signup"
            }
        })

    }
)()

async function callApi(body, url) {
    console.log({ "email": body.email });
    const response = await fetch(url, {
        method: "POST",
        mode: "cors",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    })
    return await response.json()
}

