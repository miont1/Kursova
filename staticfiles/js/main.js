    // GET Search Form and Page Links
    let searchForm = document.getElementById('searchForm')
    let pageLinks = document.getElementsByClassName('page-link')

    //IF Search Form exists
    if(searchForm){
         for (let i=0; pageLinks.length > i; i++){
         pageLinks[i].addEventListener('click', function (e) {
         e.preventDefault()

         // GET data attribute
         let page = this.dataset.page

         // ADD hidden search input to form
         searchForm.innerHTML += `<input value=${page} name="page" hidden/>`

         //SUBMIT form
         searchForm.submit()
         })
         }
    }


    let tags = document.getElementsByClassName('auto-tag')

    for(let i = 0; tags.length > i; i ++){
        tags[i].addEventListener('click', (e)=> {
            let tagId = e.target.dataset.tag
            let autoId = e.target.dataset.auto

            fetch('https://auto-shop-3dd759c39636.herokuapp.com/api/remove-tag/', {
                method:'DELETE',
                headers:{
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({'auto': autoId, 'tag': tagId})
            })
            .then(response => response.json())
            .then(data => {
                    e.target.remove()
            })
        })
    }