import os
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS  # Adicionando CORS

app = Flask(__name__)

# Permitir CORS para todos os domínios, ou apenas para o frontend específico
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})  # Substitua a URL do frontend se necessário

file_path = "Relatorio_cadop.csv"  # Verifique se o nome está correto e o arquivo está no mesmo diretório

# Verifica se o arquivo existe
if not os.path.exists(file_path):
    print(f"Erro: O arquivo {file_path} não foi encontrado!")
else:
    print(f"Arquivo {file_path} encontrado com sucesso!")
    try:
        # Usando 'on_bad_lines' em vez de 'error_bad_lines'
        df = pd.read_csv(file_path, delimiter=';', on_bad_lines='skip')
        print(df.head())  # Exibe as primeiras linhas para verificar a estrutura
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")

# Adicionando uma rota para a raiz
@app.route('/')
def home():
    return "Bem-vindo à API das Operadoras de Plano de Saúde! Use /operadoras para obter a lista de operadoras ou /operadora/<cnpj> para buscar uma operadora pelo CNPJ."

@app.route('/operadoras', methods=['GET'])
def get_operadoras():
    return jsonify(df.to_dict(orient='records'))

@app.route('/operadora/<cnpj>', methods=['GET'])
def get_operadora(cnpj):
    operadora = df[df['CNPJ'] == cnpj]
    if operadora.empty:
        return jsonify({"message": "Operadora não encontrada"}), 404
    return jsonify(operadora.to_dict(orient='records'))

@app.route('/search', methods=['GET'])
def search_operadoras():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Parâmetro de busca é obrigatório!"}), 400

    print(f"Buscando por: {query}")  # Log para depuração

    # Filtra as operadoras com base no nome_fantasia (case insensitive)
    results = df[df['nome_fantasia'].str.contains(query, case=False, na=False)]
    
    print(f"Resultados encontrados: {len(results)}")  # Quantos resultados encontrados

    if results.empty:
        return jsonify({"error": "Nenhuma operadora encontrada."}), 404
    
    return jsonify(results.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
