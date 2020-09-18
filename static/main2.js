let toggleNavStatus = false;

let toggleNav = function(){
    let getSidebar = document.querySelector(".nav-sidebar");
    let getSidebarUl = document.querySelector(".nav-sidebar ul");
    let getSidebarTitle = document.querySelector(".nav-sidebar ul li span");
    let getSidebarLinks = document.querySelectorAll(".nav-sidebar ul li a");

    if(toggleNavStatus === false){
        getSidebarUl.style.visibility = "visible";
        getSidebar.style.width = "272px";
        getSidebarTitle.style.opacity = "0.5";
        
        let arraylength = getSidebarLinks.length;
        for(var i=0;i<arraylength;i++){
            getSidebarLinks[i].style.opacity = "1";
        }

         toggleNavStatus = true;

    }

     else if(toggleNavStatus === true){
        getSidebar.style.width = "30px";
        getSidebarTitle.style.opacity = "0";
        
        let arraylength = getSidebarLinks.length;
        for(var i=0;i<arraylength;i++){
            getSidebarLinks[i].style.opacity = "0";
        }

        getSidebarUl.style.visibility = "hidden";

         toggleNavStatus = false;

    }
}

               var slideIndex = 1;
               showSlides(slideIndex);
               
               function plusSlides(n) {
                 showSlides(slideIndex += n);
               }
               
               function currentSlide(n) {
                 showSlides(slideIndex = n);
               }
               
               function showSlides(n) {
                 var i;
                 var slides = document.getElementsByClassName("mySlides");
                 var dots = document.getElementsByClassName("dot");
                 if (n > slides.length) {slideIndex = 1}    
                 if (n < 1) {slideIndex = slides.length}
                 for (i = 0; i < slides.length; i++) {
                     slides[i].style.display = "none";  
                 }
                 for (i = 0; i < dots.length; i++) {
                     dots[i].className = dots[i].className.replace(" active", "");
                 }
                 slides[slideIndex-1].style.display = "block";  
                 dots[slideIndex-1].className += " active";
               }