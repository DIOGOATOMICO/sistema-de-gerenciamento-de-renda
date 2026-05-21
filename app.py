from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime
from collections import defaultdict
from pathlib import Path
import logging

# Configuration
BASE_DIR = Path(__file__).parent
ARQUIVO = BASE_DIR / "dados.json"

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def carregar():
    """Load financial data from JSON file."""
    if ARQUIVO.exists():
        try:
            with open(ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error loading file: {e}")
            return []
    return []

def salvar(dados):
    """Save financial data with atomic write to prevent corruption."""
    try:
        temp_file = ARQUIVO.with_suffix(".tmp")
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        os.replace(temp_file, ARQUIVO)
        return True
    except IOError as e:
        logger.error(f"Error saving file: {e}")
        return False

def agrupar_por_mes(dados):
    """Group financial data by month."""
    meses = defaultdict(lambda: {"renda": 0, "gasto": 0})

    for d in dados:
        try:
            data = datetime.fromisoformat(d["data"])
        except (KeyError, ValueError, TypeError):
            logger.warning(f"Invalid date format in record: {d}")
            continue

        chave = data.strftime("%Y-%m")
        
        # Handle both old and new data structures
        if "tipo" in d:
            # New structure: separate renda/gasto
            if d["tipo"] == "renda":
                meses[chave]["renda"] += d.get("valor", 0)
            elif d["tipo"] == "gasto":
                meses[chave]["gasto"] += d.get("valor", 0)
        else:
            # Old structure: combined renda/gasto
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


def calcular_saldo(dados):
    """Calculate current balance from all records."""
    saldo = 0.0
    for d in dados:
        if d.get("tipo") == "renda":
            saldo += d.get("valor", 0)
        elif d.get("tipo") == "gasto":
            saldo -= d.get("valor", 0)
        else:
            saldo += d.get("renda", 0)
            saldo -= d.get("gasto", {}).get("valor", 0)
    return saldo


@app.route("/")
def index():
    dados = carregar()
    mensal = agrupar_por_mes(dados)
    saldo = calcular_saldo(dados)
    return render_template("index.html", dados=dados, mensal=mensal, saldo=saldo)

@app.route("/add", methods=["POST"])
def add():
    dados = carregar()

    try:
        tipo = request.form.get("tipo")
        if tipo not in ["renda", "gasto"]:
            logger.warning(f"Invalid type received: {tipo}")
            return "Tipo inválido (deve ser 'renda' ou 'gasto')", 400
        
        valor = float(request.form.get("valor", 0))
        if valor <= 0:
            return "Valor deve ser maior que zero", 400
        
        descricao = request.form.get("descricao", "sem descrição").strip()
        if not descricao:
            descricao = "sem descrição"
            
    except ValueError as e:
        logger.error(f"Error converting values: {e}")
        return "Erro nos dados enviados (valor inválido)", 400
    except Exception as e:
        logger.error(f"Unexpected error in add route: {e}")
        return "Erro nos dados enviados", 400

    registro = {
        "tipo": tipo,
        "descricao": descricao,
        "valor": valor,
        "data": datetime.now().isoformat()
    }

    dados.append(registro)
    
    if not salvar(dados):
        return "Erro ao salvar dados", 500
    
    logger.info(f"Record added: {tipo} - {valor} - {descricao}")
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
