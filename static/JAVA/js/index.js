//============ for navBar =========================================================//Start>
    const body = document.querySelector("body");
    const navbar = document.querySelector(".navbar");
    const menuBtn = document.querySelector(".menu-btn");
    const cancelBtn = document.querySelector(".cancel-btn");
    menuBtn.onclick = ()=>{
      navbar.classList.add("show");
      menuBtn.classList.add("hide");
      body.classList.add("disabled");
    }
    cancelBtn.onclick = ()=>{
      body.classList.remove("disabled");
      navbar.classList.remove("show");
      menuBtn.classList.remove("hide");
    }
    window.onscroll = ()=>{
      this.scrollY > 20 ? navbar.classList.add("sticky") : navbar.classList.remove("sticky");
    }
//============ for navBar =========================================================// End >



//============ Picture appear after 1 second =============================================//Start>
  //window.onload = function(){
    //window.setTimeout('document.getElementById("TheImgId").style.display = "inline";',500);
    //window.setTimeout('document.getElementById("TheImgId").style.display = "none";',6000);
    //window.setTimeout('document.getElementById("vidcontent").style.display = "inline";',3000);
    //window.setTimeout('document.getElementById("vid").style.display = "inline";',7000);
  //}
//============ Picture appear after 1 second =============================================// End >



//============ Album Section =============================================//Start>
function classToggle() {
  var el = document.querySelector('.icon-cards__content');
  el.classList.toggle('step-animation');
  }
  document.querySelector('#toggle-animation').addEventListener('click', classToggle);
//============ Album Section =============================================// End >


//============ Album Section =============================================//Start>
//const stopVideos = () => {
//  document.querySelectorAll('iframe').forEach(v => { v.src = v.src });
//  document.querySelectorAll('video').forEach(v => { v.pause() });
//};

//function stopVideos () {
//  document.querySelectorAll('iframe').forEach(v => { v.src = v.src });
//  document.querySelectorAll('video').forEach(v => { v.pause() });
//};
//============ Album Section =============================================// End >





//============ Section 1a. Intro =============================================// End >
function html1(img) {
var iframe3 = document.getElementById("frame3");
var img1 = document.getElementById("img1");

img1.setAttribute("class", "hidden1A");
iframe3.setAttribute("class", "shown1A");
}
//============ Section 1a. Intro =============================================// End >