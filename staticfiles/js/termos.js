document.addEventListener("DOMContentLoaded", function () {
    const modalsHTML = `
      <!-- Modal de Termos de Aceite -->
      <div class="modal fade" id="termsModal" tabindex="-1" aria-labelledby="termsModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="termsModalLabel">Termos de Aceite</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body" id="terms-body"></div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Modal de Política de Privacidade -->
      <div class="modal fade" id="privacityPolicy" tabindex="-1" aria-labelledby="privacityPolicyLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="privacityPolicyLabel">Política de Privacidade</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body" id="privacityPolicy-body"></div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
            </div>
          </div>
        </div>
      </div>
    `;
    document.body.insertAdjacentHTML("beforeend", modalsHTML);
  
    // ***CONTEUDO MODAL TERMOS DE ACEITE***
    document.getElementById("terms-body").innerHTML = `
      <h3>Termos de Aceite da Omnis Seguros</h3>
    <p><strong>Vigente a partir de 2024</strong></p>

    <p>Ao utilizar os serviços da Omnis Seguros, você concorda integralmente com os termos e condições abaixo. Recomendamos a leitura atenta deste documento antes de prosseguir.</p>

    <h4>1. Aceitação dos Termos</h4>
    <p>O uso dos serviços da Omnis Seguros está condicionado à aceitação e cumprimento destes Termos de Aceite. Caso não concorde com qualquer disposição, pedimos que não utilize nossos serviços.</p>

    <h4>2. Serviços Oferecidos</h4>
    <p>A Omnis Seguros fornece serviços de cotação e intermediação de seguros, garantindo segurança e suporte aos clientes interessados. O uso desses serviços está sujeito às regras estabelecidas por seguradoras e órgãos reguladores.</p>

    <h4>3. Cadastro e Responsabilidades</h4>
    <ul>
        <li>O usuário se compromete a fornecer informações verdadeiras, completas e atualizadas no momento do cadastro.</li>
        <li>O fornecimento de informações falsas ou incorretas pode resultar no cancelamento do serviço.</li>
        <li>A segurança das credenciais de acesso é de responsabilidade do usuário.</li>
    </ul>

    <h4>4. Uso Adequado dos Serviços</h4>
    <ul>
        <li>Os serviços devem ser utilizados exclusivamente para fins lícitos.</li>
        <li>É proibido qualquer tipo de uso indevido que possa comprometer a segurança e integridade do sistema.</li>
        <li>O descumprimento destas condições pode resultar na suspensão do acesso aos serviços.</li>
    </ul>

    <h4>5. Privacidade e Proteção de Dados</h4>
    <p>A Omnis Seguros adota medidas de segurança para proteger os dados pessoais dos usuários, conforme descrito na nossa <a href="#">Política de Privacidade</a>.</p>

    <h4>6. Limitação de Responsabilidade</h4>
    <p>A Omnis Seguros não se responsabiliza por:</p>
    <ul>
        <li>Erros causados por informações incorretas fornecidas pelo usuário.</li>
        <li>Interrupções de serviço por motivos técnicos ou de força maior.</li>
        <li>Decisões tomadas pelo usuário com base em informações fornecidas pelo site.</li>
    </ul>

    <h4>7. Alterações nos Termos</h4>
    <p>A Omnis Seguros se reserva o direito de modificar estes Termos de Aceite a qualquer momento. As alterações entrarão em vigor assim que publicadas no site. O uso contínuo dos serviços após alterações significa a aceitação dos novos termos.</p>

    <h4>8. Contato</h4>
    <p>Para dúvidas ou esclarecimentos sobre estes Termos de Aceite, entre em contato pelo e-mail <a href="mailto:contato@omnisseguros.com.br">contato@omnisseguros.com.br</a> ou pelo telefone (21) 9999-9999.</p>

    <p><strong>Ao continuar, você declara ter lido e concordado com estes Termos de Aceite.</strong></p>
    <p><strong>Omnis Seguros - Protegendo o seu futuro.</strong></p>
    `;
  



    // ***CONTEUDO MODAL POLITICA DE PRIVACIDADE***
    document.getElementById("privacityPolicy-body").innerHTML = `
          <h3>Política de Privacidade da Omnis Seguros</h3>
    <p><strong>Única e Efetiva a partir de 2024</strong></p>

    <p>A Omnis Seguros valoriza a privacidade e a segurança dos dados de seus usuários. Esta Política de Privacidade explica como coletamos, usamos, armazenamos e protegemos suas informações pessoais. Ao acessar e utilizar nossos serviços, você concorda com os termos descritos abaixo.</p>

    <h4>1. Coleta de Informações</h4>
    <p>Coletamos informações pessoais para fornecer nossos serviços de forma segura e eficiente. Os dados podem ser coletados nas seguintes situações:</p>
    <ul>
        <li>Quando você preenche formulários de contato ou cotação.</li>
        <li>Ao utilizar nosso site e interagir com nossos serviços.</li>
        <li>Por meio de cookies e tecnologias similares para melhorar sua experiência.</li>
    </ul>
    <p>As informações coletadas podem incluir: nome, CPF, data de nascimento, telefone, endereço, informações do veículo e outros dados necessários para a prestação de serviços.</p>

    <h4>2. Uso das Informações</h4>
    <p>As informações coletadas são utilizadas para:</p>
    <ul>
        <li>Processamento de cotações e fornecimento de serviços.</li>
        <li>Contato para esclarecimento de dúvidas ou envio de informações relevantes.</li>
        <li>Melhoria da segurança e da usabilidade do nosso site.</li>
        <li>Cumprimento de obrigações legais e regulatórias.</li>
    </ul>

    <h4>3. Compartilhamento de Dados</h4>
    <p>A Omnis Seguros não vende, aluga ou compartilha suas informações pessoais com terceiros, exceto nos seguintes casos:</p>
    <ul>
        <li>Quando necessário para a execução dos serviços contratados.</li>
        <li>Cumprimento de obrigações legais, judiciais ou regulatórias.</li>
        <li>Proteção de direitos, segurança e prevenção a fraudes.</li>
    </ul>

    <h4>4. Proteção e Armazenamento de Dados</h4>
    <p>Adotamos medidas técnicas e organizacionais adequadas para proteger suas informações contra acesso não autorizado, alteração, divulgação ou destruição. Seus dados são armazenados em servidores seguros e por tempo determinado conforme as normas vigentes.</p>

    <h4>5. Seus Direitos</h4>
    <p>Você tem o direito de:</p>
    <ul>
        <li>Acessar, corrigir ou excluir seus dados pessoais.</li>
        <li>Revogar seu consentimento para o uso de dados a qualquer momento.</li>
        <li>Solicitar informações sobre como seus dados são tratados.</li>
    </ul>
    <p>Para exercer esses direitos, entre em contato conosco pelo e-mail <a href="mailto:contato@omnisseguros.com.br">contato@omnisseguros.com.br</a>.</p>

    <h4>6. Cookies e Tecnologias Semelhantes</h4>
    <p>Utilizamos cookies para melhorar a experiência do usuário, analisar tráfego e personalizar conteúdo. Você pode configurar seu navegador para recusar cookies, mas isso pode afetar algumas funcionalidades do site.</p>

    <h4>7. Alterações nesta Política</h4>
    <p>Esta política pode ser atualizada periodicamente para refletir mudanças nos serviços ou na legislação. Recomendamos que você revise esta página regularmente.</p>

    <h4>8. Contato</h4>
    <p>Caso tenha dúvidas sobre esta Política de Privacidade, entre em contato conosco pelo e-mail <a href="mailto:contato@omnisseguros.com.br">contato@omnisseguros.com.br</a> ou pelo telefone (21) 9999-9999.</p>

    <p><strong>Omnis Seguros - Protegendo o seu futuro.</strong></p>
    `;

    // Exibir Modal Termos
    const termsLink = document.getElementById('termsLink');
    const termsModal = new bootstrap.Modal(document.getElementById('termsModal'));
    termsLink.addEventListener('click', function(event) {
      event.preventDefault();
      termsModal.show();
    
  });
    // Exibir Modal Privacidade
    const privacityLink = document.getElementById('policyLink');
    const privacityModal = new bootstrap.Modal(document.getElementById('privacityPolicy'));
    privacityLink.addEventListener('click', function(event) {
      event.preventDefault();
      privacityModal.show();
    });

});
  