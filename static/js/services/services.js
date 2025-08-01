function adjustImagePosition() {
    const screenWidth = window.innerWidth;
    const imgContainer = document.querySelector('.img-container');
    const heroTitle = document.getElementById('hero-title');

    if (screenWidth < 992) {
      heroTitle.insertAdjacentElement("afterend", imgContainer); 
    } else {
      const row = document.querySelector('.row');
      row.insertBefore(imgContainer, row.firstChild); 
    }
  }

  // Ajusta ao carregar e ao redimensionar a tela
  window.addEventListener("load", adjustImagePosition);
  window.addEventListener("resize", adjustImagePosition);