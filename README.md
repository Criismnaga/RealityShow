# Projeto de Inscrições para o BBB

Este projeto é uma aplicação web para gerenciar as inscrições dos participantes do BBB (Big Brother Brasil). Os usuários podem se inscrever preenchendo um formulário com suas informações, que podem ser editadas ou excluídas. A administração do BBB pode categorizar os participantes em três grupos distintos e gerenciar essas inscrições.

## Funcionalidades do Projeto

### Cadastro de Participantes
- Os participantes podem se inscrever preenchendo um formulário com informações pessoais e enviando suas respostas.
- O participante pode editar ou excluir suas informações de inscrição.

### Visualização e Categorias de Participantes
- Cada participante pode ser classificado em um dos três grupos:
  - **Pipoca**: Participantes anônimos, sem reconhecimento público.
  - **Camarote**: Participantes que já têm alguma visibilidade ou fama.
  - **Não Selecionado**: Participantes que ainda não foram classificados para o programa.

### Visualizações e Permissões
- **Participante**: Usuários que se inscrevem podem visualizar, editar ou excluir suas inscrições.
- **Administrador (ADM)**: Usuários com permissão de administrador podem ver todas as inscrições, categorizar os participantes nos grupos, editar ou excluir inscrições, e fazer a seleção final dos participantes.

### Banco de Dados
- O banco de dados armazena as informações de cada participante e suas inscrições.
- Estrutura das tabelas com entidades para gerenciar as inscrições e as informações dos participantes.

## Requisitos Técnicos
- **CRUD Completo** para gerenciar inscrições (criação, leitura, atualização e exclusão).
- **Sistema de Autenticação** para diferenciar entre participante e administrador.
- **Banco de Dados Relacional** (MySQL ou outro compatível) para armazenar dados dos participantes.
- **Docker e Docker Compose** para facilitar o desenvolvimento e a execução da aplicação.

## Fluxo de Trabalho

### Inscrição e Edição de Participantes
1. Participantes se inscrevem e preenchem o formulário.
2. Podem revisar e editar suas informações até o fim do período de inscrição.

### Revisão e Classificação pelo Administrador
1. Administradores têm acesso a todas as inscrições e podem categorizar os participantes nos grupos Pipoca, Camarote ou Não Selecionado.
2. Podem editar e ajustar informações ou status das inscrições e excluir se necessário.

## Implementação e Execução

### Pré-requisitos
- Docker
- Docker Compose
- Python 3.9+ com pip

### Passos para Configuração e Execução

1. **Clone o repositório e navegue até o diretório do projeto**
   ```bash
   git clone <url-do-repositorio>
   cd <caminho-para-o-diretorio-do-projeto>
   ```

2. **Configuração do Ambiente Virtual**
   Crie e ative um ambiente virtual para instalar as dependências:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows, use: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Execute o Projeto com Docker Compose**
   No diretório onde está o `docker-compose.yml`, execute o comando:
   ```bash
   docker-compose up --build
   ```

4. **Acessando a API**
   Acesse a API FastAPI no navegador ou via cliente HTTP em [http://localhost:8000](http://localhost:8000).

5. **Executando o Docker Compose para Iniciar o Banco de Dados**
   Iniciar o Docker Compose:
   ```bash
   docker-compose up --build  # Reconstrói e inicia os contêineres
   ```

6. **Verificando o Banco de Dados**
   Execute o seguinte comando em um segundo terminal:
   ```bash
   docker exec -it fccpd-mod2-db-1 mysql -u root -p
   ```
   Insira os comandos SQL (exemplo):
   ```sql
   USE fccpd;
   SHOW TABLES;
   SELECT * FROM participantes;
   ```
   Digite `exit` para sair.

7. **Reinicializando o Docker Compose**
   Caso faça alguma alteração no script, siga os passos abaixo:
   - Rode `docker-compose down -v` no segundo terminal
   - Pressione `Control+C` no primeiro terminal
   - Depois, repita os comandos de inicialização.
