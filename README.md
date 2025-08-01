# Projeto Omnis  
- O Omnis foi um website de seguros desenvolvido durante as aulas de Python do curso Transfero Academy 2025. No website é possível fazer uma cotação rápida de seguros, e o sistema calcula o valor do seguro de acordo com os dados fornecidos.
  
![Tela inicial](https://github.com/Roberto-Lourenco/django_projeto_omnis/blob/main/website_preview/home_preview_hero.png)
---

## Tecnologias Utilizadas

- Python (Django)
- JavaScript
- CSS
- HTML

---

## Estrutura do Projeto

O projeto está organizado nas seguintes pastas principais:

- `base/global` — Configurações e funcionalidades globais do projeto.
- `contato` — Módulo relacionado a formulários e funcionalidades de contato (Em desenvolvimento).
- `contratos` — Gestão de contratos dentro do sistema (Em desenvolvimento).
- `home` — Página inicial e conteúdo principal.
- `omnis` — Pasta de configurações do projeto.
- `planos` — Funcionalidades relacionadas a planos de seguros.
- `resultadoCotacao` — Apresentação dos resultados das cotações.
- `servicos` — Serviços oferecidos pelo seguro.
- `static` e `staticfiles` — Arquivos estáticos do projeto (JS, CSS, imagens).
- `templates/admin` — Templates para a interface administrativa.
- `usuarios` — Módulo de autenticação e gerenciamento de usuários.
- `website_preview` — Pré-visualização do website em desenvolvimento.

---

## Como Rodar o Projeto

### Pré-requisitos

- Python 3.11+
- Pip
- Virtualenv (opcional, mas recomendado)

### Passos para executar

1. Clone o repositório:
    ```bash
    git clone https://github.com/SeuUsuario/django_projeto_omnis.git
    cd django_projeto_omnis
    ```

2. Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate     # Windows
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Execute as migrações:
    ```bash
    python manage.py migrate
    ```

5. Inicie o servidor de desenvolvimento:
    ```bash
    python manage.py runserver
    ```

6. Acesse o site no navegador:
    ```
    http://127.0.0.1:8000/
    ```

---

## Funcionalidades

- Cotação rápida de seguros com cálculo automático (Geração de PDF em desenvolvimento).
- Gestão de planos e contratos(Em desenvolvimento).
- Área de contato para suporte e dúvidas(Em desenvolvimento).
- Interface administrativa para gerenciamento do sistema.
- Autenticação e gerenciamento de usuários.

---

## Observações

>Este projeto foi desenvolvido como parte do curso Transfero Academy 2025 e serve apenas como exemplo prático para aprendizado de desenvolvimento web com Django.

