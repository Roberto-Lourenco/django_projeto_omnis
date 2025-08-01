// Selecionar modelo do veículo
const marcas = {
    volkswagen:["Gol","Polo","Jetta","Voyage","Virtus"],
    fiat:["Argo","Cronos","Gran Siena","Mobi","Strada","Toro" ],
    chevrolet:["Cruze","Onix","Prisma","Spin","Tracker"]
};
const marcaForms = document.getElementById("marca");
const modeloForms = document.getElementById("modelo");

marcaForms.addEventListener("change", function(){
    const marcaAtual = marcaForms.value;

    modeloForms.innerHTML = `<option value="">Modelo do veículo</option>`

    if(marcas[marcaAtual]){
        marcas[marcaAtual].forEach(function(modelo){
            const newOption = document.createElement("option");
            newOption.value = modelo.toLowerCase();
            newOption.textContent = modelo;
            modeloForms.appendChild(newOption);

        });

    const cpfValido = validarCPF(cpf);
    const errorMessage = document.getElementById('cpfError');
    
    if (!cpfValido) {
      errorMessage.style.display = 'inline'; 
    } else {
      errorMessage.style.display = 'none'; 
    }
    }
});

// Validar cpf
function validarCPF(cpf) {

    cpf = cpf.replace(/\D/g, '');
  

    if (cpf.length !== 11) return false;
    if (/^(\d)\1{10}$/.test(cpf)) return false;
  
    let soma = 0;
    let resto;
  
    for (let i = 1; i <= 9; i++) {
      soma += parseInt(cpf[i - 1]) * (11 - i);
    }

    resto = (soma * 10) % 11;
    if (resto === 10 || resto === 11) resto = 0;
    if (resto !== parseInt(cpf[9])) return false;
    soma = 0;
  

    for (let i = 1; i <= 10; i++) {
      soma += parseInt(cpf[i - 1]) * (12 - i);
    }

    resto = (soma * 10) % 11;
    if (resto === 10 || resto === 11) resto = 0;
    if (resto !== parseInt(cpf[10])) return false;

    return true;
  }

  
// Padronizar cpf
document.getElementById('cpf').addEventListener('input', function(e) {
    let cpf = e.target.value.replace(/\D/g, ''); 

    if (cpf.length <= 11) {
      cpf = cpf.replace(/(\d{3})(\d)/, '$1.$2');
      cpf = cpf.replace(/(\d{3})(\d)/, '$1.$2');
      cpf = cpf.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    }
    e.target.value = cpf;

    // Valida o CPF
    const cpfValido = validarCPF(cpf);
    const errorMessage = document.getElementById('cpfError');
    
    if (!cpfValido) {
      errorMessage.style.display = 'block'; 
      
    } else {
      errorMessage.style.display = 'none'; 
    }
  });

  // Padronizar e validar CEP
document.getElementById("cep").addEventListener("input", function(e) {
  let cep = e.target.value.replace(/\D/g, ""); 
  if (cep.length <= 8) {
      cep = cep.replace(/(\d{5})(\d)/, "$1-$2");
  }
  e.target.value = cep;

  // Valida o CEP
  validarCEP(cep);
});

// Validação de CEP (apenas checa se tem 8 dígitos numéricos e consulta API)
function validarCEP(cep) {
  cep = cep.replace(/\D/g, '');
  const errorMessageCep = document.getElementById('cepError');

  if (!/^[0-9]{8}$/.test(cep)) {
      errorMessageCep.style.display = 'block'; 
      errorMessageCep.innerText = "Formato de CEP inválido";
      return false;
  }
  errorMessageCep.style.display = 'none';

  pesquisacep(cep);
  return true;
}

// Consultar ViaCEP
let endereco = {};
function meu_callback(conteudo) {
  const errorMessageCep = document.getElementById('cepError');

  if (!("erro" in conteudo)) {
      endereco = {
          rua: conteudo.logradouro,    
          bairro: conteudo.bairro,     
          cidade: conteudo.localidade, 
          uf: conteudo.uf,  
          ibge: conteudo.ibge
      };
      console.log(endereco);
      errorMessageCep.style.display = 'none'; // Esconde o erro se encontrar o CEP
  } else {
      console.log("CEP não encontrado");
      errorMessageCep.style.display = 'block'; 
      errorMessageCep.innerText = "CEP não encontrado";
  }
}

function pesquisacep(valor) {
  var cep = valor.replace(/\D/g, '');

  if (cep !== "") {
      if (/^[0-9]{8}$/.test(cep)) {
          var script = document.createElement('script');
          script.src = 'https://viacep.com.br/ws/' + cep + '/json/?callback=meu_callback';
          document.body.appendChild(script);
      }
  }
}




//   Padronizar celular
const inputTelefone = document.getElementById("telefone");

inputTelefone.addEventListener("input", function () {
  let telefone = inputTelefone.value;
  telefone = telefone.replace(/\D/g, ""); // Remove tudo que não for número

  if (telefone.length > 0) {
    if (telefone.length <= 2) {
      telefone = telefone.replace(/^(\d{0,2})/, "($1");
    } else if (telefone.length <= 7) {
      telefone = telefone.replace(/^(\d{2})(\d{0,5})/, "($1) $2");
    } else if (telefone.length <= 10) {
      telefone = telefone.replace(/^(\d{2})(\d{1})(\d{0,4})/, "($1) $2$3");
    } else {
      telefone = telefone.replace(/^(\d{2})(\d{1})(\d{4})(\d{0,4})/, "($1) $2$3-$4");
    }
  }

  inputTelefone.value = telefone;
});

// Capturando dados do forms e redirecionamento

document.getElementById("form-cotacao").addEventListener("submit", function(e){
  e.preventDefault();

  const cpfError = document.getElementById('cpfError');
  const cepError = document.getElementById('cepError');

  const cpfErrorDisplay = window.getComputedStyle(cpfError).display;
  const cepErrorDisplay = window.getComputedStyle(cepError).display;

 

  if(cpfErrorDisplay === 'block'){
    cpfError.textContent = "Valide o CPF antes de enviar.";
    return;
  }
  if(cepErrorDisplay === 'block'){
    cepError.textContent = "Valide o CEP antes de enviar.";
    return;
  }


  let dadosForm = {
    nome: document.getElementById("name").value.toLowerCase(),
    cpf: document.getElementById("cpf").value,
    dataNasc: document.getElementById("dataNasc").value,
    telefone: document.getElementById("telefone").value,
    cep: document.getElementById("cep").value,
    endereco:endereco,
    marcaVeiculo: document.getElementById("marca").value,
    modeloVeiculo: document.getElementById("modelo").value.split(" ").join("_").toLowerCase(),
    anoVeiculo: document.getElementById("ano-auto").value,
    termosCheck: document.getElementById("termos").checked
  };

  localStorage.setItem("cotacaoData",JSON.stringify(dadosForm));

  window.location.href = "/resultadoCotacao";
});

