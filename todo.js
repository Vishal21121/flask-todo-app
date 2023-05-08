(function(){
    document.getElementById('submit').addEventListener("click", (e)=>{
        let val = document.getElementById("input").value
        addVal(val)
    })
    
    document.getElementById('input').addEventListener("keyup", (event)=>{
        let val = document.getElementById("input").value
        if (event.key === 'Enter') {
            console.log(val);
            addVal(val)
        }
    })
    addVal()
})()

async function todoFetch(){
    let userid = localStorage.getItem("userid")
    const response = await fetch(`http://localhost:8081/getTodo/${userid}`)
    return response
}



async function addVal(){
    let response = await todoFetch()
    let data = await response.json()
    data.data.forEach(({title}) => {
        document.getElementById("todoContainer").innerHTML += `
    <div
                class="w-1/2 bg-gray-900 ml-40 p-2 my-4 rounded-3xl flex justify-center focus:border-5 border-5 border-red-800 ">
                <div class="w-full">
                    <input type="text"
                        class="bg-gray-900  w-11/12 text-gray-400 h-8 border-none focus:outline-none pl-4"
                        placeholder="What's your next task?" value="${title}">
                </div>
                <button
                    class="text-gray-400 outline outline-blue-700 rounded-xl py-0.5 font-semibold px-4  hover:bg-blue-700 hover:text-white mt-1 mr-4">EDIT
                </button>
                <button
                    class="text-gray-400 outline outline-red-700 rounded-xl py-0.5 font-semibold px-4  hover:bg-red-700 hover:text-white mt-1 mr-4">DELETE
                </button>
    </div>`
    });
    
    document.getElementById("input").value = ''
}