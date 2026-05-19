from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO = os.path.join(BASE_DIR, "dados.json") 

app = Flask(__name__)

def carregar():
    if os.path.exists(ARQUIVO):
        try:
            with open(ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def salvar(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def agrupar_por_mes(dados):
    meses = defaultdict(lambda: {"renda": 0, "gasto": 0})

    for d in dados:
        try:
            data = datetime.fromisoformat(d["data"])
        except (KeyError, ValueError, TypeError):
            continue

        chave = data.strftime("%Y-%m")
        meses[chave]["renda"] += d.get("renda", 0)
        meses[chave]["gasto"] += d.get("gasto", {}).get("valor", 0)

    resultado = []
    for mes, valores in meses.items():
        resultado.append({
            "mes": mes,
            "renda": valores["renda"],
            "gasto": valores["gasto"],
            "sobra": valores["renda"] - valores["gasto"]
        })

    return sorted(resultado, key=lambda x: x["mes"])

@app.route("/")
def index():
    dados = carregar()
    mensal = agrupar_por_mes(dados)
    return render_template("index.html", dados=dados, mensal=mensal)

@app.route("/add", methods=["POST"])
def add():
    dados = carregar()

    try:
        renda = float(request.form.get("renda", 0))
        descricao = request.form.get("descricao", "sem descrição")
        valor = float(request.form.get("valor", 0))
    except:
        return "Erro nos dados enviados", 400

    registro = {
        "renda": renda,
        "gasto": {
            "descricao": descricao,
            "valor": valor
        },
        "data": datetime.now().isoformat()
    }

    dados.append(registro)
    salvar(dados)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=False)