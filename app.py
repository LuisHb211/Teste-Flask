from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from db_connection import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

SECRET_KEY = os.getenv('SECRET_KEY')

if SECRET_KEY is None:
    raise ValueError("A chave secreta não foi definida no arquivo .env")

app.secret_key = SECRET_KEY

class Produto:
    def __init__(self, id, nome, descricao, preco):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        
    @staticmethod
    def buscar_todos():
        """
        Método estático para buscar todos os produtos no banco de dados.
        Retorna uma lista de objetos Produto.
        """
        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM produto")
        produtos = cursor.fetchall()
        cursor.close()
        lista_produtos = []
        for produto in produtos:
            lista_produtos.append(Produto(*produto))
        return lista_produtos

    @staticmethod
    def buscar_por_id(id):
        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM produto WHERE id = %s", (id,))
        produto = cursor.fetchone()
        cursor.close()
        if produto:
            return Produto(*produto)
        return None

    def salvar(self):
        """
        Método para salvar as alterações de um produto no banco de dados.
        """
        cnx = get_db_connection()
        cursor = cnx.cursor()
        query = "UPDATE produto SET nome=%s, descricao=%s, preco=%s WHERE id=%s"
        cursor.execute(query, (self.nome, self.descricao, self.preco, self.id))
        cnx.commit()
        cursor.close()
        
    @staticmethod
    def criar(nome, descricao, preco):
        """
        Método estático para criar um novo produto no banco de dados.
        Retorna um objeto Produto criado.
        """
        cnx = get_db_connection()
        cursor = cnx.cursor()
        query = "INSERT INTO produto (nome, descricao, preco) VALUES (%s, %s, %s)"
        cursor.execute(query, (nome, descricao, preco))
        cnx.commit()
        id = cursor.lastrowid  
        cursor.close()
        return Produto(id, nome, descricao, preco)
    
    @staticmethod
    def deletar(id):
        """
        Método estático para deletar um produto do banco de dados pelo ID.
        """
        cnx = get_db_connection()
        cursor = cnx.cursor()
        query = "DELETE FROM produto WHERE id = %s"
        cursor.execute(query, (id,))
        cnx.commit()
        cursor.close()

@app.route('/produtos', methods=['GET'])
def get_produtos():
    """
    Endpoint para obter todos os produtos.
    Retorna uma lista de produtos se o usuário estiver logado, caso contrário, redireciona para a página de login.
    """
    if 'logged_in' in session and session['logged_in']:
        produtos = Produto.buscar_todos()
        lista_produtos = [produto.__dict__ for produto in produtos]
        return jsonify(lista_produtos)
    else:
        return render_template('login.html')

@app.route('/produtos', methods=['POST'])
def add_produto():
    """
    Endpoint para adicionar um novo produto.
    Recebe os dados do produto no formato JSON e os adiciona ao banco de dados.
    Retorna uma mensagem de sucesso e os dados do produto adicionado.
    """
    novo_produto = request.json
    nome = novo_produto['nome']
    descricao = novo_produto['descricao']
    preco = novo_produto['preco']
    produto = Produto.criar(nome, descricao, preco)
    
    #produto.__dict__ é um objeto da classe Produto retornado em forma de dicionário contendo os atributos do objeto
    return jsonify({'mensagem': 'Produto adicionado com sucesso', 'produto': produto.__dict__}), 201

@app.route('/produtos/<int:id>', methods=['PUT'])
def update_produto(id):
    """
    Endpoint para atualizar um produto existente.
    Recebe os dados do produto atualizado no formato JSON e os atualiza no banco de dados.
    Retorna uma mensagem de sucesso e os dados do produto atualizado.
    """
    produto_atualizado = request.json
    produto = Produto.buscar_por_id(id)
    if produto:
        produto.nome = produto_atualizado['nome']
        produto.descricao = produto_atualizado['descricao']
        produto.preco = produto_atualizado['preco']
        produto.salvar()
        return jsonify({'mensagem': 'Produto atualizado com sucesso', 'produto': produto_atualizado})
    return jsonify({'mensagem': 'Produto não encontrado'}), 404

@app.route('/produtos/<int:id>', methods=['DELETE'])
def delete_produto(id):
    """
    Endpoint para excluir um produto existente.
    Exclui o produto do banco de dados pelo ID.
    Retorna uma mensagem de sucesso.
    """
    Produto.deletar(id)
    return jsonify({'mensagem': 'Produto excluído com sucesso'}), 200

@app.route('/')
def produtos():
    '''
    Verifica se o usuário está logado, verificando se a chave 'logged_in' está presente na sessão
    e se está definida como True
    '''
    if 'logged_in' in session and session['logged_in']:
        produtos = Produto.buscar_todos()
        return render_template('home.html', produtos=produtos)
    else:
        return redirect(url_for('login'))

@app.route('/editar/<int:id>')
def editar(id):
    produto = Produto.buscar_por_id(id)
    return render_template('editar_produto.html', produto=produto)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        
        try:
            cnx = get_db_connection()
            cursor = cnx.cursor()
            query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, email, hashed_password))
            cnx.commit()
            cursor.close()
            cnx.close()
            return redirect(url_for('login'))
        except Exception as e:
            return jsonify({'erro': str(e)}), 500
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'] #obtém o email enviado no formulário
        password = request.form['password'] # obtém a senha enviada no formulário

        try:
            cnx = get_db_connection() 
            cursor = cnx.cursor()
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone() #busca o usuário com o email fornecido no banco de dados

            if user and check_password_hash(user[3], password):
                # Autenticação bem-sucedida
                session['logged_in'] = True
                session['user_email'] = email
                return redirect(url_for('produtos'))  #Redireciona para a rota '/'

        except Exception as e:
            return jsonify({'erro': str(e)}), 500
        
    #Renderiza a página de login caso a requisição seja do tipo GET
    return render_template('login.html', erro="Credenciais inválidas")

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return render_template('login.html')

if __name__ == "__main__":
    app.run()