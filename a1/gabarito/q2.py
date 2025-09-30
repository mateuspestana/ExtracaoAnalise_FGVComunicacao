# Questão 2 - API de Biblioteca Digital com FastAPI
# Objetivo: criar uma API simples com 2 endpoints usando FastAPI.
# - Endpoint 1: /biblioteca/info -> retorna info da biblioteca
# - Endpoint 2: /biblioteca/livro/{livro_id} -> retorna dados do livro por ID
# Observação: não é necessário executar o servidor aqui, apenas escrever o código.

from fastapi import FastAPI
from typing import Optional, List, Dict, Any

# Criando a aplicação FastAPI
app = FastAPI(title="Biblioteca Digital API", version="1.0.0")

# Base de dados de livros (lista de dicionários)
# Atenção: havia um erro de sintaxe no item 7 ("titulo:"), aqui corrigimos para "titulo"
livros_db: List[Dict[str, Any]] = [
    {"id": 1, "titulo": "1984", "autor": "George Orwell", "ano": 1949, "paginas": 328, "genero": "Ficção Científica", "disponivel": True},
    {"id": 2, "titulo": "Dom Casmurro", "autor": "Machado de Assis", "ano": 1899, "paginas": 256, "genero": "Romance", "disponivel": False},
    {"id": 3, "titulo": "O Pequeno Príncipe", "autor": "Antoine de Saint-Exupéry", "ano": 1943, "paginas": 96, "genero": "Fábula", "disponivel": True},
    {"id": 4, "titulo": "Cem Anos de Solidão", "autor": "Gabriel García Márquez", "ano": 1967, "paginas": 417, "genero": "Realismo Mágico", "disponivel": True},
    {"id": 5, "titulo": "Fahrenheit 451", "autor": "Ray Bradbury", "ano": 1953, "paginas": 249, "genero": "Ficção Científica", "disponivel": False},
    {"id": 6, "titulo": "O Cortiço", "autor": "Aluísio Azevedo", "ano": 1890, "paginas": 304, "genero": "Naturalismo", "disponivel": True},
    {"id": 7, "titulo": "Hypnerotomachia Poliphili", "autor": "Francesco Colonna", "ano": 1499, "paginas": 700, "genero": "Ficção", "disponivel": False},
]

# Endpoint 1: /biblioteca/info
# Retorna nome da biblioteca, total de livros e uma mensagem de boas-vindas
@app.get("/biblioteca/info")
def info_biblioteca() -> Dict[str, Any]:
    total = len(livros_db)
    resposta = {
        "nome": "Biblioteca Digital FGV Comunicação Rio",
        "total_livros": total,
        "mensagem": "Bem-vindo à nossa biblioteca digital!",
    }
    return resposta

# Endpoint 2: /biblioteca/livro/{livro_id}
# Procura o livro pelo ID. Se encontrar, retorna o livro inteiro.
# Se não encontrar, retorna um dicionário com erro.
@app.get("/biblioteca/livro/{livro_id}")
def buscar_livro(livro_id: int) -> Dict[str, Any]:
    for livro in livros_db:
        if livro.get("id") == livro_id:
            return livro
    # Se não achou, devolve uma mensagem de erro simples
    return {"erro": f"Livro com ID {livro_id} não encontrado"}

# Observação para execução local (opcional):
# Para rodar o servidor: uvicorn q2:app --reload
# (Certifique-se de estar na pasta correta e ter fastapi e uvicorn instalados.)
