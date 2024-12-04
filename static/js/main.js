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
