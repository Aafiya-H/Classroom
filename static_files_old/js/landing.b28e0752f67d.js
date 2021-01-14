let slideIndex = 1;
// showSlides(slideIndex);

function changeSlide(n) {
  showSlides(slideIndex += n);
}

function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("info-slide");
  var dots = document.getElementsByClassName("dot");
  if (n > slides.length) 
  slideIndex = 1;

  if (n < 1) 
  slideIndex = slides.length;

  for (i = 0; i < slides.length; i++) {
    if (i==slideIndex-1)
    slides[i].style.display = "block";

    else
    slides[i].style.display = "none";  
  }
  for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
  }
  // slides[slideIndex-1].style.display = "block";  
  dots[slideIndex-1].className += " active";
}

window.onload = function() {
    showSlides(slideIndex);
}