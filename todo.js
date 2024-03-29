(function () {

    if (!localStorage.getItem("userid")) {
        window.location.href = window.origin + "/login"
    }
    insertTodos()

    document.getElementById('submit').addEventListener("click", (e) => {
        let val = document.getElementById("input").value
        if (val.length > 0) {
            addTodo(val)
        }
    })

    document.getElementById('input').addEventListener("keyup", (event) => {
        let val = document.getElementById("input").value
        if (event.key === 'Enter') {
            console.log(val);
            if (val.length > 0) {
                addTodo(val)
            }
        }
    })
    console.log(document.getElementById("delete"));
})()

// ! TODO
async function deleteTodo(deleatable) {
    Array.from(deleatable).forEach(element => {
        element.addEventListener("click", async (element) => {
            const id = element.target.parentNode.firstElementChild.firstElementChild.id
            const response = await fetch(`http://localhost:8081/deleteTodo/${id}`, { method: "DELETE" })
            const data = await response.json()
            console.log(data);
            if (data["status"] == "success") {
                console.log(data["message"]);
                insertTodos()
            }
        })
    });
}

async function updateTodo(editable) {
    Array.from(editable).forEach((element) => {
        element.addEventListener("click", (event) => {
            const buttonEl = document.createElement("button");
            buttonEl.classList.add("text-gray-400", "outline", "outline-orange-700", "rounded-xl", "py-0.5", "font-semibold", "px-4", "hover:bg-orange-600", "hover:text-white", "mt-1", "mr-4", "delete");
            buttonEl.id = "save"
            buttonEl.textContent = "SAVE";
            event.target.parentNode.appendChild(buttonEl);
            let contentElement = event.target.parentNode.firstElementChild.firstElementChild
            contentElement.setAttribute("contenteditable", "true")
            document.getElementById('save').addEventListener("click", async () => {
                let val = contentElement.innerText
                let todoId = contentElement.id
                const response = await fetch(`http://localhost:8081/updateTodo/${todoId}`, {
                    method: 'cors',
                    method: "PATCH",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ "title": val })
                })
                insertTodos()
            })

        })
    })
}

function addListener() {
    let deleatable = document.getElementsByClassName("delete")
    deleteTodo(deleatable)
    let editable = document.getElementsByClassName("edit")
    updateTodo(editable)

}

async function todoFetch() {
    let userid = localStorage.getItem("userid")
    const response = await fetch(`http://localhost:8081/getTodo/${userid}`)
    return response
}

async function addTodo(val) {
    let userid = localStorage.getItem("userid")
    let response = await fetch(`http://localhost:8081/addTodo/${userid}`, {
        mode: 'cors',
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ "title": val })
    })
    let data = await response.json()
    let id = data["data"]
    console.log(id);
    insertTodoId(val, id)
}

async function insertTodoId(title, id) {
    //TODO: add svgs in place of buttons
    document.getElementById("todoContainer").innerHTML += `
    <div
                class="w-1/2 bg-gray-900 ml-40 p-2 my-4 rounded-3xl flex justify-center focus:border-5 border-5 border-red-800 ">
                <div class="w-full">
                    <p class="bg-gray-900  w-11/12 text-gray-400 h-8 border-none focus:outline-none pl-4 align-middle"
                        placeholder="What's your next task?" id="${id}">${title}</p>
                </div>
                <button
                    class="text-gray-400 outline outline-blue-700 rounded-xl py-0.5 font-semibold px-4  hover:bg-blue-700 hover:text-white mt-1 mr-4 edit">EDIT
                </button>
                <button
                    class="text-gray-400 outline outline-red-700 rounded-xl py-0.5 font-semibold px-4  hover:bg-red-700 hover:text-white mt-1 mr-4 delete" >DELETE
                </button>
    </div>`
    addListener()
    document.getElementById("input").value = ''
}

async function insertTodos() {
    let response = await todoFetch()
    let data = await response.json()
    document.getElementById("todoContainer").innerHTML = ''
    data.data.forEach(({ title, todoId }) => {
        //TODO: add svgs in place of buttons
        document.getElementById("todoContainer").innerHTML += `
            <div
                class="w-1/2 bg-gray-900 ml-40 p-2 my-4 rounded-3xl flex justify-center focus:border-5 border-5 border-red-800 ">
                <div class="w-full">
                    <p class="bg-gray-900  w-11/12 text-gray-400 h-8 border-none focus:outline-none pl-4 align-middle" id="${todoId}">${title}</p>
                </div>
                <button
                    class="text-gray-400 outline outline-blue-700 rounded-xl py-0.5 font-semibold px-4  hover:bg-blue-700 hover:text-white mt-1 mr-4 edit">EDIT
                </button>
                <button
                    class="text-gray-400 outline outline-red-700 rounded-xl py-0.5 font-semibold px-4  hover:bg-red-700 hover:text-white mt-1 mr-4 delete" >DELETE
                </button>
            </div>`
    });
    addListener()
    document.getElementById("input").value = ''

}

// TODO: add logout functionality
document.getElementById("logout").addEventListener("click", () => {
    localStorage.removeItem("userid")
    window.location.href = window.origin + "/login"
})