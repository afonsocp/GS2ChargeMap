from flask import Flask, request, jsonify
from flask_cors import CORS
import cx_Oracle

app = Flask(__name__)
CORS(app)


dsn = cx_Oracle.makedsn("oracle.fiap.com.br", 1521, service_name="ORCL")  
connection = cx_Oracle.connect(user="rm557705", password="290805", dsn=dsn)

@app.route("/informacoes", methods=["GET"])
def get_informacoes():
    cursor = connection.cursor()
    cursor.execute("SELECT id, nome_completo, TO_CHAR(data_nascimento, 'YYYY-MM-DD') AS data_nascimento, email, cep FROM informacoes")
    rows = cursor.fetchall()
    cursor.close()
    informacoes = [
        {"id": row[0], "nome_completo": row[1], "data_nascimento": row[2], "email": row[3], "cep": row[4]}
        for row in rows
    ]
    return jsonify(informacoes)

@app.route("/informacoes", methods=["POST"])
def add_informacao():
    data = request.json
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO informacoes (nome_completo, data_nascimento, email, cep)
        VALUES (:nome_completo, TO_DATE(:data_nascimento, 'YYYY-MM-DD'), :email, :cep)
        """,
        nome_completo=data["nome_completo"],
        data_nascimento=data["data_nascimento"],
        email=data["email"],
        cep=data["cep"],
    )
    connection.commit()
    cursor.close()
    return jsonify({"message": "Informação adicionada com sucesso"}), 201

@app.route("/informacoes/<int:id>", methods=["PUT"])
def update_informacao(id):
    data = request.json
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE informacoes
        SET nome_completo = :nome_completo,
            data_nascimento = TO_DATE(:data_nascimento, 'YYYY-MM-DD'),
            email = :email,
            cep = :cep
        WHERE id = :id
        """,
        id=id,
        nome_completo=data["nome_completo"],
        data_nascimento=data["data_nascimento"],
        email=data["email"],
        cep=data["cep"],
    )
    connection.commit()
    cursor.close()
    return jsonify({"message": "Informação atualizada com sucesso"})

@app.route("/informacoes/<int:id>", methods=["DELETE"])
def delete_informacao(id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM informacoes WHERE id = :id", id=id)
    connection.commit()
    cursor.close()
    return jsonify({"message": "Informação excluída com sucesso"})

if __name__ == "__main__":
    app.run(debug=True)
