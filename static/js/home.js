function ajustarFundo() {
  const heroSection = document.getElementById("cta");
  const vetorHero = document.getElementById("vetor-hero");

  const isMobile = window.innerWidth < 993;

  if (isMobile) {
    heroSection.style.backgroundImage = "";
    heroSection.style.backgroundColor = "#f8f9fa";
    vetorHero.style.display = "flex";
  } else {
    heroSection.style.backgroundImage = `url(${bannerHomeUrl})`;
    vetorHero.style.display = "none";
  }
}

window.addEventListener("resize", ajustarFundo);
ajustarFundo();

