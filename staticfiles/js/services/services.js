function adjustImagePosition() {
    const screenWidth = window.innerWidth;
    const imgContainer = document.querySelector('.img-container');
    const heroTitle = document.getElementById('hero-title');
    const heroText = document.getElementById('hero-text');

    if (screenWidth < 992) { // Se for menor que 992px (tela pequena)
      heroTitle.insertAdjacentElement("afterend", imgContainer); // Move a imagem abaixo do título
    } else {
      const row = document.querySelector('.row');
      row.insertBefore(imgContainer, row.firstChild); // Volta a imagem para a posição original
    }
  }

  // Ajusta ao carregar e ao redimensionar a tela
  window.addEventListener("load", adjustImagePosition);
  window.addEventListener("resize", adjustImagePosition);