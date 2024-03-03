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
        cnx = get_db_connection()
        cursor = cnx.cursor()
        query = "UPDATE produto SET nome=%s, descricao=%s, preco=%s WHERE id=%s"
        cursor.execute(query, (self.nome, self.descricao, self.preco, self.id))
        cnx.commit()
        cursor.close()
        
    @staticmethod
    def criar(nome, descricao, preco):
        cnx = get_db_connection()
        cursor = cnx.cursor()
        query = "INSERT INTO produto (nome, descricao, preco) VALUES (%s, %s, %s)"
        cursor.execute(query, (nome, descricao, preco))
        cnx.commit()
        id = cursor.lastrowid  # Obtém o ID do último produto inserido
        cursor.close()
        return Produto(id, nome, descricao, preco)
    
    @staticmethod
    def deletar(id):
        cnx = get_db_connection()
        cursor = cnx.cursor()
        query = "DELETE FROM produto WHERE id = %s"
        cursor.execute(query, (id,))
        cnx.commit()
        cursor.close()

@app.route('/produtos', methods=['GET'])
def get_produtos():
    if 'logged_in' in session and session['logged_in']:
        produtos = Produto.buscar_todos()
        lista_produtos = [produto.__dict__ for produto in produtos]
        return jsonify(lista_produtos)
    else:
        return render_template('login.html')

@app.route('/produtos', methods=['POST'])
def add_produto():
    novo_produto = request.json
    nome = novo_produto['nome']
    descricao = novo_produto['descricao']
    preco = novo_produto['preco']
    produto = Produto.criar(nome, descricao, preco)
    return jsonify({'mensagem': 'Produto adicionado com sucesso', 'produto': produto.__dict__}), 201

@app.route('/produtos/<int:id>', methods=['PUT'])
def update_produto(id):
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
    Produto.deletar(id)
    return jsonify({'mensagem': 'Produto excluído com sucesso'}), 200

@app.route('/')
def produtos():
    if 'logged_in' in session and session['logged_in']:
        produtos = Produto.buscar_todos()
        return render_template('home.html', produtos=produtos)
    else:
        return render_template('login.html')

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
        email = request.form['email']
        password = request.form['password']

        try:
            cnx = get_db_connection()  # Supondo que você tenha uma função get_db_connection() definida em algum lugar
            cursor = cnx.cursor()
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()

            if user and check_password_hash(user[3], password):
                # Autenticação bem-sucedida
                session['logged_in'] = True
                session['user_email'] = email
                return redirect(url_for('produtos'))  # Redireciona para a rota '/'
            else:
                # Autenticação inválidas
                return jsonify({'erro': 'Credenciais inválidas'}), 401

        except Exception as e:
            return jsonify({'erro': str(e)}), 500

    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return render_template('login.html')

if __name__ == "__main__":
    app.run()