let URL = 'https://auto-shop-3dd759c39636.herokuapp.com/'


let form = document.getElementById('login-form')

form.addEventListener('submit', (e) => {
    e.preventDefault()

    let formData = {
    'username':form.username.value,
    'password':form.password.value
    }

    fetch('https://auto-shop-3dd759c39636.herokuapp.com/api/users/token/', {
        method: "POST",
        headers:{
        "Content-Type": "application/json",
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then (data => {
        if (data.access){
        localStorage.setItem('token', data.access)
        window.location = 'http://localhost:63342/firstDjango/frontend/autos-list.html'
        }else{
        alert('Username OR password wrong')
        }
    })


})