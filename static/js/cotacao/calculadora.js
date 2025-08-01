import { carrosFipe } from "./fipeVeiculos.js";

let receberFormCalc = localStorage.getItem("cotacaoData");

if (receberFormCalc) {
  let frmCalculadora = JSON.parse(receberFormCalc);

  // Dados do usuário
  let nascimento = new Date(frmCalculadora.dataNasc);
  let idade = calcularIdade(nascimento);
  let cepUser = parseInt(frmCalculadora.cep, 10);

  // Dados do veículo
  let marca = frmCalculadora.marcaVeiculo;
  let modelo = frmCalculadora.modeloVeiculo;
  let ano = frmCalculadora.anoVeiculo;

  let valorPlanos = {
    basico: 1.3,
    completo: 1.5,
    premium: 1.8,
  };

  function calcularValorFipe(fipeBase) {
  return fipeBase * 0.4;
}
let valorFipe = calcularValorFipe(carrosFipe[marca][modelo][ano]);

  exibirValoresNoHtml(valorFipe, idade, cepUser, valorPlanos);

  localStorage.removeItem("cotacaoData");
}

// === Funções Utilitárias ===

function calcularIdade(nascimento) {
  const anoAtual = new Date().getFullYear();
  return anoAtual - nascimento.getFullYear();
}

function calcularSeguro(fipe, idade, cepUser, valorBase) {
  let acrescimos = calcularAcrescimos(idade, cepUser);
  return ((fipe * acrescimos) / 100) / 12 * valorBase;
}

function calcularAcrescimos(idade, cep) {
  const acrescimoRegiao = calcularAcrescimoPorRegiao(cep);
  const acrescimoIdade = calcularAcrescimoPorIdade(idade);

  return acrescimoRegiao + acrescimoIdade;
}

function calcularAcrescimoPorRegiao(cep) {
  if (isBetween(cep, 20000, 23799)) return 8;
  if (isBetween(cep, 23800, 26600)) return 10;
  if (isBetween(cep, 26601, 28999)) return 3;
  return 0;
}

function calcularAcrescimoPorIdade(idade) {
  if (isBetween(idade, 18, 26)) return 8;
  if (isBetween(idade, 27, 43)) return 4;
  if (isBetween(idade, 44, 65)) return 5;
  return 8; // abaixo de 18 ou acima de 65
}

function isBetween(value, min, max) {
  return value >= min && value <= max;
}

function exibirValoresNoHtml(valorFipe, idade, cepUser, valorPlanos) {
  const valores = {
    basico: calcularSeguro(valorFipe, idade, cepUser, valorPlanos.basico),
    completo: calcularSeguro(valorFipe, idade, cepUser, valorPlanos.completo),
    premium: calcularSeguro(valorFipe, idade, cepUser, valorPlanos.premium),
  };

  document.getElementById("valor-basico").innerHTML = `R$ ${valores.basico.toFixed(2)}`;
  document.getElementById("valor-intermediario").innerHTML = `R$ ${valores.completo.toFixed(2)}`;
  document.getElementById("valor-premium").innerHTML = `R$ ${valores.premium.toFixed(2)}`;
}
