let URL = 'https://auto-shop-3dd759c39636.herokuapp.com/'

let loginBtn = document.getElementById('login-btn')
let logoutBtn = document.getElementById('logout-btn')

let token = localStorage.getItem('token')

if (token) {
    loginBtn.remove()
} else {
    logoutBtn.remove()
}
logoutBtn.addEventListener('click', (e) => {
    e.preventDefault()
    localStorage.removeItem('token')
    window.location = 'http://localhost:63342/firstDjango/frontend/login.html'
})


let autosUrl = 'https://auto-shop-3dd759c39636.herokuapp.com/api/autos/'

let getAutos = () => {
fetch(autosUrl)
.then(response => response.json())
.then (data => {
buildAutos(data)
})
}

let buildAutos = (autos) => {
let autosWrapper = document.getElementById('autos--wrapper')
autosWrapper.innerHTML = ""
for (let i = 0; autos.length > i; i++){
let auto = autos[i]

let autoCard = `
<div class="auto--card">
<img src = "https://auto-shop-3dd759c39636.herokuapp.com/${auto.featured_image}">
<div>
    <div class="card--header">
    <h3>${auto.car_brand} ${auto.car_model}</h3>
    <strong class="vote--option" data-vote="like" data-auto="${auto.id}" >&#43;</strong>
    <strong class="vote--option" data-vote="dislike" data-auto="${auto.id}" >&#8722;</strong>
    </div>
<i>${auto.vote_ratio}% Positive Feedback</i>
<p>${auto.description.substring(0,150)}</p>
</div>
</div>
`
autosWrapper.innerHTML += autoCard
}
// Listener
addVoteEvents()

}

let addVoteEvents = () => {
    let token = localStorage.getItem('token')
    let voteBtns = document.getElementsByClassName('vote--option');
    for (let i = 0; i < voteBtns.length; i++) {
        voteBtns[i].addEventListener('click', (e) => {
            let vote = e.target.dataset.vote;
            let auto = e.target.dataset.auto;

            fetch(`https://auto-shop-3dd759c39636.herokuapp.com/api/autos/${auto}/vote/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`
                },
                 body: JSON.stringify({ 'value': vote })

            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                getAutos()
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
};


getAutos()