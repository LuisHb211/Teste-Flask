# Api, CRUD e sistema de login

Aplicação desenvolvida em Python, FLASK e MySQL

## Instalação

Para clonar o repositório na sua máquina basta clonar:
```
git clone link
```
É necessário criar uma variável de ambiente, ativa-la e instalar os requisitos.
No terminal do projeto, após ter clonado-o:
```
python -m venv venv
```
```
.\venv\Scripts\activate 
```
```
pip install -r requirements.txt 
```
Como esse projeto está baseado em um crud e sistema de login, foi utilizado o MySQL para o seu desenvolvimento, assim, para linkar o projeto com o banco de dados, é essencial criar um arquivo .env na base do projeto e colocar as informações do banco de dados:
```
USER=seuUsuario
PASSWORD=suaSenha
HOST=SeuHost
DATABASE=SeuBanco
```
Além disso, é necessário criar duas tabelas no banco de dados, sendo elas a tablea 'produto' e a tabela 'users',
tabela produto deve ter 'id', 'nome', 'descricao', 'preco'
tabela users deve ter 'id', 'name', 'email', 'password'
É de extrema importância que tenham o mesmo nome descrito anteriormente.

Após ter completado os requisitos, basta abrir o arquivo app.py e executá-lo. Caso esteja no Visual Studio Code, vá em "Run Python File". No canto superior direito, clique na seta apontando para baixo ao lado do botão de reprodução, ou simplesmente pressione F5. No console, será exibido o local/porta em que o programa está sendo executado. Basta abri-lo no navegador da internet, ou segurar Ctrl e clicar no link.


## Explicando o código

O arquivo db_connection.py tem a finalidade de estabelecer uma conexão com um banco de dados MySQL. Ele é responsável por carregar as informações de acesso ao banco de dados a partir de um arquivo .env, utilizando a função load_dotenv, e então utiliza essas credenciais para estabelecer a conexão com o banco de dados por meio da biblioteca mysql.connector.

Em app.py contém o código principal da aplicação Flask, incluindo as rotas, as definições de comportamento das rotas e a inicialização da aplicação. As rotas são definidas utilizando o decorator @app.route(). Cada rota direciona para uma URL e os métodos HTTP que ela aceita. As funções associadas a cada rota são chamadas quando a rota correspondente é acessada. Ao iniciar o programa o usuário é redirecionado para a rota('/'), nela será verificado se o usuário está logado, caso contrário ele será redirecionado para a tela de login. Por se tratar de uma aplicaçao mais simples, a api, e a aplicaçao do CRUD com suas rotas foram colocadas todas em app.py, sem uma pasta para models.py. 

O design do front-end foi o mais básico possível, já que o intuito principal era a parte do back-end, além de não ter domínio mais robusto com html e css.


## 🛠️ Construído com

* [Visual Studo Code](https://code.visualstudio.com/) - Editor de texto 
* [Python](https://www.python.org/) - Linguagem usada
* [FLASK]([https://fastapi.tiangolo.com/](https://flask.palletsprojects.com/en/3.0.x/)) - Framework usado
* [GIT](https://git-scm.com/) - Controle de versionamento
* [MySQL](https://www.mysql.com/) - Banco de Dados

## 🎁 Conclusão

* Projeto desenvolvido para desenvolver sistema de CRUD, API e login, além de utilizar o framework Flask
* Compreensão de API's, git e variáveis de ambientes, framework, banco de dados;
