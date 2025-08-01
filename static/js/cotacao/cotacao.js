document.addEventListener('DOMContentLoaded', function () {
  // ==============================================
  // 1. ELEMENTOS DO FORMULÁRIO
  // ==============================================
  const marcaSelect = document.getElementById('id_marca');
  const modeloSelect = document.getElementById('id_modelo');
  const anoSelect = document.getElementById('id_ano');
  const versaoSelect = document.getElementById('id_versao');
  const cpfInput = document.getElementById('cpf');
  const cpfError = document.getElementById('cpfError');
  const cepInput = document.getElementById('cep');
  const cepError = document.getElementById('cepError');
  const telefoneInput = document.getElementById('telefone');
  const formCotacao = document.getElementById('form-cotacao');

  // ==============================================
  // 2. FUNÇÕES AUXILIARES
  // ==============================================

  function updateDynamicSelect(select, options, defaultText, selectedValue = null) {
    const currentValue = select.value;
    select.innerHTML = `<option value="">${defaultText}</option>`;

    options.forEach(option => {
      const opt = document.createElement('option');
      opt.value = option;
      opt.textContent = option;
      select.appendChild(opt);
    });

    if (options.includes(currentValue)) {
      select.value = currentValue;
    } else if (selectedValue && options.includes(selectedValue)) {
      select.value = selectedValue;
    } else if (selectedValue && !options.includes(selectedValue)) {
      const opt = document.createElement('option');
      opt.value = selectedValue;
      opt.textContent = selectedValue;
      opt.selected = true;
      select.appendChild(opt);
    }

    select.disabled = false;
  }

  function resetSelect(select, placeholder) {
    select.innerHTML = `<option value="">${placeholder}</option>`;
    select.disabled = true;
  }

  function makeFetchRequest(url, successCallback) {
    fetch(url, {
      headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        'Accept': 'application/json'
      },
      credentials: 'include'
    })
      .then(response => {
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return response.json();
      })
      .then(successCallback)
      .catch(error => {
        console.error('Erro na requisição:', error);
        ['modeloSelect', 'anoSelect', 'versaoSelect'].forEach(select => {
          resetSelect(window[select], 'Erro ao carregar dados');
        });
      });
  }

  // ==============================================
  // 3. EVENTOS DOS SELECTS DINÂMICOS
  // ==============================================

  marcaSelect.addEventListener('change', function () {
    if (!this.value) {
      resetSelect(modeloSelect, 'Selecione o modelo');
      resetSelect(anoSelect, 'Selecione o ano');
      resetSelect(versaoSelect, 'Selecione a versão');
      return;
    }

    makeFetchRequest(`/get-modelos/?marca=${encodeURIComponent(this.value)}`, data => {
      updateDynamicSelect(modeloSelect, data.modelos, 'Selecione o modelo', modeloSelect.dataset.selectedValue);
      resetSelect(anoSelect, 'Selecione o ano');
      resetSelect(versaoSelect, 'Selecione a versão');
    });
  });

  modeloSelect.addEventListener('change', function () {
    if (!this.value || !marcaSelect.value) {
      resetSelect(anoSelect, 'Selecione o ano');
      resetSelect(versaoSelect, 'Selecione a versão');
      return;
    }

    makeFetchRequest(`/get-anos/?marca=${encodeURIComponent(marcaSelect.value)}&modelo=${encodeURIComponent(this.value)}`, data => {
      updateDynamicSelect(anoSelect, data.anos, 'Selecione o ano', anoSelect.dataset.selectedValue);
      resetSelect(versaoSelect, 'Selecione a versão');
    });
  });

  anoSelect.addEventListener('change', function () {
    if (!this.value || !marcaSelect.value || !modeloSelect.value) {
      resetSelect(versaoSelect, 'Selecione a versão');
      return;
    }

    makeFetchRequest(`/get-versoes/?marca=${encodeURIComponent(marcaSelect.value)}&modelo=${encodeURIComponent(modeloSelect.value)}&ano=${encodeURIComponent(this.value)}`, data => {
      updateDynamicSelect(versaoSelect, data.versoes, 'Selecione a versão', versaoSelect.dataset.selectedValue);
    });
  });

  // ==============================================
  // 4. VALIDAÇÕES DE FORMULÁRIO
  // ==============================================

  cpfInput.addEventListener('input', function (e) {
    let cpf = e.target.value.replace(/\D/g, '');
    if (cpf.length > 0) {
      cpf = cpf.replace(/(\d{3})(\d)/, '$1.$2')
               .replace(/(\d{3})(\d)/, '$1.$2')
               .replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    }
    e.target.value = cpf;
    cpfError.style.display = validarCPF(cpf) ? 'none' : 'block';
  });

  function validarCPF(cpf) {
    cpf = cpf.replace(/\D/g, '');
    if (cpf.length !== 11 || /^(\d)\1{10}$/.test(cpf)) return false;

    let soma = 0;
    for (let i = 0; i < 9; i++) soma += parseInt(cpf.charAt(i)) * (10 - i);
    let resto = (soma * 10) % 11;
    if (resto === 10 || resto === 11) resto = 0;
    if (resto !== parseInt(cpf.charAt(9))) return false;

    soma = 0;
    for (let i = 0; i < 10; i++) soma += parseInt(cpf.charAt(i)) * (11 - i);
    resto = (soma * 10) % 11;
    if (resto === 10 || resto === 11) resto = 0;
    return resto === parseInt(cpf.charAt(10));
  }

  cepInput.addEventListener('input', function (e) {
    let cep = e.target.value.replace(/\D/g, '');
    if (cep.length > 0) {
      cep = cep.replace(/^(\d{5})(\d)/, '$1-$2');
    }
    e.target.value = cep;

    if (cep.replace(/\D/g, '').length === 8) {
      pesquisacep(cep.replace(/\D/g, ''));
    }
  });

  function pesquisacep(cep) {
    const script = document.createElement('script');
    script.src = `https://viacep.com.br/ws/${cep}/json/?callback=meuCallback`;
    document.body.appendChild(script);
  }

  window.meuCallback = function (conteudo) {
    if (!("erro" in conteudo)) {
      document.getElementById('logradouro').value = conteudo.logradouro || '';
      document.getElementById('bairro').value = conteudo.bairro || '';
      document.getElementById('cidade').value = conteudo.localidade || '';
      document.getElementById('uf').value = conteudo.uf || '';
      cepError.style.display = 'none';
    } else {
      cepError.style.display = 'block';
      cepError.textContent = "CEP não encontrado";
    }
  };

  telefoneInput.addEventListener('input', function () {
    let telefone = this.value.replace(/\D/g, '');

    if (telefone.length > 0) {
      if (telefone.length <= 2) {
        telefone = telefone.replace(/^(\d{0,2})/, '($1');
      } else if (telefone.length <= 7) {
        telefone = telefone.replace(/^(\d{2})(\d{0,5})/, '($1) $2');
      } else if (telefone.length <= 10) {
        telefone = telefone.replace(/^(\d{2})(\d{1})(\d{0,4})/, '($1) $2$3');
      } else {
        telefone = telefone.replace(/^(\d{2})(\d{1})(\d{4})(\d{0,4})/, '($1) $2$3-$4');
      }
    }

    this.value = telefone;
  });

  // ==============================================
  // 5. INICIALIZAÇÃO COM DADOS PRÉ-SELECIONADOS
  // ==============================================

  function initializeForm() {
    if (marcaSelect.dataset.selectedValue) marcaSelect.value = marcaSelect.dataset.selectedValue;
    if (modeloSelect.dataset.selectedValue) modeloSelect.value = modeloSelect.dataset.selectedValue;
    if (anoSelect.dataset.selectedValue) anoSelect.value = anoSelect.dataset.selectedValue;
    if (versaoSelect.dataset.selectedValue) versaoSelect.value = versaoSelect.dataset.selectedValue;

    if (marcaSelect.value) {
      makeFetchRequest(`/get-modelos/?marca=${encodeURIComponent(marcaSelect.value)}`, data => {
        updateDynamicSelect(modeloSelect, data.modelos, 'Selecione o modelo', modeloSelect.dataset.selectedValue);

        if (modeloSelect.value) {
          makeFetchRequest(`/get-anos/?marca=${encodeURIComponent(marcaSelect.value)}&modelo=${encodeURIComponent(modeloSelect.value)}`, data => {
            updateDynamicSelect(anoSelect, data.anos, 'Selecione o ano', anoSelect.dataset.selectedValue);

            if (anoSelect.value) {
              makeFetchRequest(`/get-versoes/?marca=${encodeURIComponent(marcaSelect.value)}&modelo=${encodeURIComponent(modeloSelect.value)}&ano=${encodeURIComponent(anoSelect.value)}`, data => {
                updateDynamicSelect(versaoSelect, data.versoes, 'Selecione a versão', versaoSelect.dataset.selectedValue);
              });
            }
          });
        }
      });
    }
  }

  initializeForm();

  // ==============================================
  // 6. VALIDAÇÃO FINAL ANTES DO SUBMIT
  // ==============================================

  formCotacao.addEventListener('submit', function (e) {
    if (!validarCPF(cpfInput.value.replace(/\D/g, ''))) {
      e.preventDefault();
      cpfError.textContent = "CPF inválido";
      cpfError.style.display = 'block';
      cpfInput.focus();
      return;
    }

    if (cepInput.value.replace(/\D/g, '').length !== 8 || cepError.style.display === 'block') {
      e.preventDefault();
      cepError.textContent = "CEP inválido";
      cepError.style.display = 'block';
      cepInput.focus();
      return;
    }

    if (!marcaSelect.value || !modeloSelect.value || !anoSelect.value || !versaoSelect.value) {
      e.preventDefault();
      alert('Por favor, preencha todos os campos do veículo');
    }
  });
});
