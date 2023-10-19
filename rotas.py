from flask import Flask, jsonify, request
from datetime import datetime
import sqlite3


app = Flask(__name__)

db_path = 'bd_pizzaria.sqlite'


############### CLIENTES #############

@app.route('/clientes')
def obter_clientes():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Clientes")
        rows = cursor.fetchall()
        readings = []
        for row in rows:
            reading = {
                'id_cliente': row[0],
                'nome': row[1],
                'morada': row[2],
                'telefone': row[3]
            }
            readings.append(reading)
        return jsonify(readings)

@app.route('/clientes/<int:id_cliente>')
def obter_clientes_by_id(id_cliente):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Clientes WHERE id_cliente = ?", (id_cliente,))
        rows = cursor.fetchall()
        cliente = {}
        if rows:
            cliente = {
                'id_cliente': rows[0][0],
                'nome': rows[0][1],
                'morada': rows[0][2],
                'telefone': rows[0][3]
            }
            return cliente
        else:
            return {'message': 'Cliente nao encontrado'}

        
@app.route('/clientes', methods=['POST'])
def criar_cliente():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        dados = request.json
        if dados is None:
            return {'message': 'Dados do cliente ausentes ou inválidos'}, 400
        nome = dados.get('nome')
        morada = dados.get('morada')
        telefone = dados.get('telefone')
        if nome is None or morada is None or telefone is None:
            return {'message': 'Dados do cliente incompletos'}, 400
        cursor.execute("INSERT INTO Clientes (nome, morada, telefone) VALUES (?, ?, ?)", (nome, morada, telefone))
        conn.commit()
        novo_id = cursor.lastrowid
        novo_cliente = {
            'id_cliente': novo_id,
            'nome': nome,
            'morada': morada,
            'telefone': telefone
        }
        return novo_cliente, 201

@app.route('/clientes/<int:id_cliente>', methods=['PUT'])
def atualizar_cliente(id_cliente):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        dados = request.json
        if dados is None:
            return {'message': 'Dados do cliente ausentes ou inválidos'}, 400
        nome = dados.get('nome')
        morada = dados.get('morada')
        telefone = dados.get('telefone')
        if nome is None or morada is None or telefone is None:
            return {'message': 'Dados do cliente incompletos'}, 400
        cursor.execute("""
            UPDATE Clientes SET nome = ?, morada = ?, telefone = ?
            WHERE id_cliente = ?
        """, (nome, morada, telefone, id_cliente))
        if cursor.rowcount == 0:
            return {'message': 'Cliente não encontrado'}, 404
        conn.commit()
        return {'message': f'Cliente com ID {id_cliente} atualizado com sucesso'}, 200

##############################################



############### PIZZAS #############

@app.route('/pizzas', methods=['POST'])
def criar_pizza():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        dados = request.json
        if dados is None:
            return {'message': 'Dados da pizza ausentes ou inválidos'}, 400
        nome = dados.get('nome')
        ingredientes = dados.get('ingredientes')
        if nome is None or ingredientes is None:
            return {'message': 'Dados da pizza incompletos'}, 400
        cursor.execute("INSERT INTO Pizzas (nome, ingredientes) VALUES (?, ?)", (nome, ingredientes))
        conn.commit()
        novo_id = cursor.lastrowid
        nova_pizza = {
            'id_pizza': novo_id,
            'nome': nome,
            'ingredientes': ingredientes
        }
        return nova_pizza, 201

@app.route('/pizzas', methods=['GET'])
def listar_pizzas():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Pizzas")
        pizzas = []
        for pizza in cursor.fetchall():
            pizza_dict = {
                'nome': pizza[0],
                'ingredientes': pizza[1],
            }
            pizzas.append(pizza_dict)
        return {'pizzas': pizzas}
    
#############################################



############### ENCOMENDAS #############



@app.route('/encomendas', methods=['POST'])
def criar_encomenda():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        dados = request.json
        if dados is None:
            return {'message': 'Dados da encomenda ausentes ou inválidos'}, 400
        id_cliente = dados.get('id_cliente')
        nome_pizza = dados.get('nome_pizza')
        quantidade = dados.get('quantidade')
        tamanho = dados.get('tamanho')
        data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if id_cliente is None or nome_pizza is None or quantidade is None or tamanho is None:
            return {'message': 'Dados da encomenda incompletos'}, 400
        cursor.execute("INSERT INTO Encomendas (id_cliente, nome_pizza, quantidade, tamanho, data_hora) VALUES (?, ?, ?, ?, ?)",
                       (id_cliente, nome_pizza, quantidade, tamanho, data_hora))
        conn.commit()
        novo_id = cursor.lastrowid
        nova_encomenda = {
            'id_encomenda': novo_id,
            'id_cliente': id_cliente,
            'nome_pizza': nome_pizza,
            'quantidade': quantidade,
            'tamanho': tamanho,
            'data_hora': data_hora
        }
        return nova_encomenda, 201

"""
EXEMPLO DE POST P/ ENCOMENDA

{
  "id_cliente": 7,
  "nome_pizza": "Campeão",
  "quantidade": 2,
  "tamanho": "Grande"
}

"""
    

@app.route('/encomendas', methods=['GET'])
def listar_encomendas():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Encomendas ORDER BY data_hora ASC")
        encomendas = cursor.fetchall()
        lista_encomendas = []
        for encomenda in encomendas:
            id_cliente, nome_pizza, quantidade, tamanho, data_hora = encomenda
            encomenda_dict = {
                'id_cliente': id_cliente,
                'nome_pizza': nome_pizza,
                'quantidade': quantidade,
                'tamanho': tamanho,
                'data_hora': data_hora
            }
            lista_encomendas.append(encomenda_dict)
        return {'encomendas': lista_encomendas}



############################################

if __name__ == '__main__':
    app.run(debug=True)