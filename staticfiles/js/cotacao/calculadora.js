import { carrosFipe } from "./fipeVeiculos.js";

let receberFormCalc = localStorage.getItem("cotacaoData");

if(receberFormCalc){
    let frmCalculadora = JSON.parse(receberFormCalc);

    // Dados do user para calculos
    let nascimento = new Date(frmCalculadora.dataNasc);
    let idade = 2025 - nascimento.getFullYear();
    let cepUser = frmCalculadora.cep;
    // Dados do veiculo
    let marca = frmCalculadora.marcaVeiculo;
    let modelo = frmCalculadora.modeloVeiculo;
    let ano = frmCalculadora.anoVeiculo;
    let valorFipe = carrosFipe[marca][modelo][ano]*0.4; // FIPE
    let valorPlanos = {
        basico: 1.3,
        completo: 1.5,
        premium: 1.8
    }

    // Calcular valor do seguro
    function calcularSeguro(fipe,idade,cepUser,valorBase){

        let acrescimos = 0;
        // Região
        if(cepUser >= 20000 && cepUser <= 26600){
            acrescimos += 10;
        } else if(cepUser >=26601 && cepUser <= 28999){
            acrescimos += 3;
        } else if(cepUser >= 20000 && cepUser <= 23799){
            acrescimos +=8;
        }
        // Idade
        if(idade >= 18 && idade <= 26){
            acrescimos += 8;
        } else if(idade >=27 && idade <= 43){
            acrescimos += 4;
        } else if(idade >= 44 && idade <= 65){
            acrescimos +=5;
        } else{
            acrescimos +=8;
        }

        return (fipe*acrescimos/100)/12*valorBase;
    }

    // Exibir valores no html
    document.getElementById("valor-basico").innerHTML = `R$ ${calcularSeguro(valorFipe,idade,cepUser,valorPlanos.basico).toFixed(2)}`;
    document.getElementById("valor-intermediario").innerHTML = `R$ ${calcularSeguro(valorFipe,idade,cepUser,valorPlanos.completo).toFixed(2)}`;
    document.getElementById("valor-premium").innerHTML = `R$ ${calcularSeguro(valorFipe,idade,cepUser,valorPlanos.premium).toFixed(2)}`;

} 

localStorage.removeItem("cotacaoData");