(
    function(){
        document.getElementById("signin").addEventListener("click",async ()=>{
            let email = document.getElementById("email").value
            let password = document.getElementById("password").value
            let response = await fetch("http://localhost:8081/login",{
                    headers:{"Content-Type":"application/json"},
                    method: "POST",
                    body: JSON.stringify({
                        "email": email,
                        "password": password
                    })
            })
            let data = await response.json()
            if (data["status"]=="success"){
                let userid = data["data"]
                console.log(userid);
                localStorage.setItem("userid", userid)
                location.href = location.origin + "/todo.html"
            }else{
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
            setTimeout(()=>{
                document.getElementById("alert").innerHTML = ''
            },3000)
            }
           
        })
        //  adding the elements inside the same login form
        // document.getElementById("signup").addEventListener("click",()=>{
        //     let p = document.createElement("p")
        //     p.setAttribute("class","text-lg text-white mx-12")
        //     p.innerText = "Name"
        //     console.log(p);
        //     let input = document.createElement("input")
        //     input.setAttribute("type","text")
        //     input.setAttribute("class","w-full rounded-2xl h-9 text-white bg-[rgb(71,121,190,0.3)] focus:outline-none text-center")
        //     let div = document.createElement("div")
        //     div.setAttribute("class","w-3/4 mx-auto mt-1 bg-[rgb(71,121,190,0.3)] rounded-2xl items-center")
        //     div.append(input)
        //     console.log(div);
        //     document.getElementById("pemail").parentNode.insertBefore(p,document.getElementById("pemail"))
        //     document.getElementById("pemail").parentNode.insertBefore(div,document.getElementById("pemail"))
        // })
    }
)()

