function captalizeNome(nome) {
    let primeiroNome = nome.trim().split(" ")[0]; 
    return primeiroNome.charAt(0).toUpperCase() + primeiroNome.slice(1).toLowerCase();
}

function capitalizeNomeCompleto(nome) {
    return nome
        .split(" ")
        .map(palavra => palavra.charAt(0).toUpperCase() + palavra.slice(1).toLowerCase())
        .join(" ");
}

function captalizePalavra(nome) {
    return nome.charAt(0).toUpperCase() + nome.slice(1).toLowerCase();
}

function formatarData(data) {
    const partes = data.split("-");
    const dataFormatada = `${partes[2]}/${partes[1]}/${partes[0]}`;
    return dataFormatada;
}


let receberForm = localStorage.getItem("cotacaoData");

if(receberForm){
    let frmUser = JSON.parse(receberForm);

    // Primeiro nome do usuario
    document.getElementById("primeiroNome").innerText = captalizeNome(frmUser.nome);

    // Dados pessoais usuario
    document.getElementById("resultadoNomeCliente").innerText = capitalizeNomeCompleto(frmUser.nome);
    document.getElementById("resultadoCpfCliente").innerText = frmUser.cpf;
    document.getElementById("resultadoDataNascCliente").innerText = formatarData(frmUser.dataNasc);
    document.getElementById("resultadoTelefoneCliente").innerText = frmUser.telefone;
    document.getElementById("resultadoTelefoneCliente").innerText = frmUser.telefone;

    // Endereço
    document.getElementById("resultadoLogradouro").innerText = frmUser.endereco.rua;
    document.getElementById("resultadoBairro").innerText = frmUser.endereco.bairro;
    document.getElementById("resultadoCidade").innerText = frmUser.endereco.cidade;
    document.getElementById("resultadoEstado").innerText = frmUser.endereco.uf;

    // Veiculo cotado
    document.getElementById("resultadoMarca").innerText = captalizePalavra(frmUser.marcaVeiculo);
    document.getElementById("resultadoModelo").innerText = captalizePalavra(frmUser.modeloVeiculo).split("_").join(" ");
    document.getElementById("resultadoAno").innerText = frmUser.anoVeiculo;

    console.log(frmUser.endereco.rua)

}
