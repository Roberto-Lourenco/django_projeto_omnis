const messages = document.querySelectorAll('.alert');

// Configura o timeout para cada mensagem
messages.forEach(function (message) {
  setTimeout(function () {
    // Adiciona efeito de fade out
    message.style.transition = 'opacity 0.5s';
    message.style.opacity = '0';
    setTimeout(function () {
      message.remove();
    }, 500);
  }, 3000);  // 3000ms = 3 segundos
});


// Mascaras de input
document.addEventListener('DOMContentLoaded', function () {
  const cepInput = document.getElementById('id_cep');
  const cpfCnpjInput = document.getElementById('id_cpf') || document.getElementById('id_cnpj');;

  if (cepInput) mascaraCEP(cepInput);
  if (cpfCnpjInput) mascaraCpfCnpj(cpfCnpjInput);
});

function mascaraCEP(input) {
  input.addEventListener('input', function (e) {
    let v = e.target.value.replace(/\D/g, '');
    if (v.length > 5) {
      v = v.slice(0, 5) + '-' + v.slice(5, 8);
    }
    e.target.value = v;
  });
}

function mascaraCpfCnpj(input) {
  input.addEventListener('input', function (e) {
    let v = e.target.value.replace(/\D/g, '');

    if (v.length <= 11) { // CPF
      v = v.replace(/(\d{3})(\d)/, '$1.$2');
      v = v.replace(/(\d{3})(\d)/, '$1.$2');
      v = v.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    } else { // CNPJ
      v = v.slice(0, 14); // limita máximo 14 dígitos
      v = v.replace(/^(\d{2})(\d)/, '$1.$2');
      v = v.replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3');
      v = v.replace(/\.(\d{3})(\d)/, '.$1/$2');
      v = v.replace(/(\d{4})(\d)/, '$1-$2');
    }
    e.target.value = v;
  });
}

// Mascara de telefone

document.addEventListener("DOMContentLoaded", () => {
  const telefoneInput = document.getElementById('id_telefone');

  if (!telefoneInput) return;

  telefoneInput.addEventListener('input', (event) => {
    const rawValue = event.target.value;
    const formattedValue = formatarTelefone(rawValue);
    event.target.value = formattedValue;
  });
});

function formatarTelefone(valor) {
  const numeros = valor.replace(/\D/g, '');

  if (numeros.length === 0) return '';

  if (numeros.length <= 2) {
    return `(${numeros}`;
  }

  if (numeros.length <= 7) {
    return `(${numeros.slice(0, 2)}) ${numeros.slice(2)}`;
  }

  if (numeros.length <= 10) {
    return `(${numeros.slice(0, 2)}) ${numeros.slice(2, 3)}${numeros.slice(3)}`;
  }

  return `(${numeros.slice(0, 2)}) ${numeros.slice(2, 3)}${numeros.slice(3, 7)}-${numeros.slice(7, 11)}`;
}


//PAGE LOADER
  window.addEventListener("load", function () {
    const loader = document.getElementById("loader");

    // Tempo mínimo de exibição em milissegundos
    const TEMPO_MINIMO = 200;

    const tempoInicial = performance.now();

    // Calcula quanto tempo levou para carregar
    const tempoCarregado = performance.now() - tempoInicial;
    const tempoRestante = TEMPO_MINIMO - tempoCarregado;

    // Garante que o loader fique visível pelo tempo mínimo
    setTimeout(() => {
      loader.classList.add("hidden");
    }, tempoRestante > 0 ? tempoRestante : 0);
  });

  document.addEventListener("DOMContentLoaded", () => {
    const anchors = document.querySelectorAll("a:not([target='_blank']):not([href^='#'])");
    anchors.forEach(a => {
      a.addEventListener("click", () => {
        document.getElementById("loader").classList.remove("hidden");
      });
    });
  });







