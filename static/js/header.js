/*=============== SHOW MENU ===============*/
const headerScope = document.querySelector('.no-bootstrap-header');

if (headerScope) {
  const navMenu = headerScope.querySelector('#nav-menu'),
        navToggle = headerScope.querySelector('#nav-toggle'),
        navClose = headerScope.querySelector('#nav-close');

  /* Menu show */
  if (navToggle) {
    navToggle.addEventListener('click', () => {
      navMenu.classList.add('show-menu');
    });
  }

  /* Menu hidden */
  if (navClose) {
    navClose.addEventListener('click', () => {
      navMenu.classList.remove('show-menu');
    });
  }

  /*=============== REMOVE MENU MOBILE ===============*/
  const navLinks = headerScope.querySelectorAll('.nav__link');

  navLinks.forEach(n =>
    n.addEventListener('click', () => {
      navMenu.classList.remove('show-menu');
    })
  );

  /*=============== SHOW DROPDOWN ===============*/
  const dropdown = headerScope.querySelector('#dropdown');
  if (dropdown) {
    dropdown.addEventListener('click', () => {
      dropdown.classList.toggle('show-dropdown');
    });
  }
}

/*=============== MENU FLUTUANTE ===============*/
const fab = document.getElementById('cotacaoFab');
const chatbox = document.getElementById('cotacaoChat');
const wrapper = document.getElementById('cotacaoHintWrapper');

if (fab && chatbox && wrapper) {
  console.log('Elementos cotacaoFab, cotacaoChat e cotacaoHintWrapper encontrados.');

  const clickSound = new Audio(clickSoundSrc);

  // Apenas abre e fecha o chatbox (sem som)
  fab.addEventListener('click', () => {
    console.log('FAB clicado');
    chatbox.classList.toggle('hidden');
  });

  const hintShown = sessionStorage.getItem('cotacaoHintShown');

  if (!hintShown) {
    setTimeout(() => {
      console.log('Mostrando hint inicial');
      wrapper.style.display = 'flex';
      clickSound.play();
      sessionStorage.setItem('cotacaoHintShown', 'true');

      setTimeout(() => {
        console.log('Escondendo hint inicial');
        wrapper.style.display = 'none';
      }, 6000);
    }, 2000);
  }
} else {
  console.warn('Algum elemento cotacaoFab, cotacaoChat ou cotacaoHintWrapper não foi encontrado:', { fab, chatbox, wrapper });
}