//Media query for js
var m_query = window.matchMedia("(max-width: 520px)");

//To toggle navbar on smaller screens
let nav_toggle_btn = document.querySelector("#nav-toggle-btn");
let links = document.querySelector(".links");

nav_toggle_btn.addEventListener("click", function(){
    links.classList.toggle("links-open");
    if (m_query.matches){
        links.classList.toggle("links-open-s");
    }
})

//To open/close pop up
let web_pop = document.querySelector(".web_pop");
let web_pop_btn = document.querySelector(".web_pop_btn");
let web_pop_sm = document.querySelector(".web_pop_sm");
let web_pop_btn_sm = document.querySelector(".web_pop_btn_sm");

//For bigger screens
setTimeout(function(){
    web_pop.classList.add("web_pop_open") 
}, 2000);
web_pop_btn.addEventListener("click", function(){
    web_pop.classList.remove("web_pop_open");
})

//For smaller screens
setTimeout(function(){
    if (m_query.matches){
        web_pop_sm.classList.add("web_pop_open")
    }
}, 2000)
web_pop_btn_sm.addEventListener("click", function(){
    web_pop_sm.classList.remove("web_pop_open")
})
