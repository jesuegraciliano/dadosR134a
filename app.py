import math
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# --- Constantes e Funções de Cálculo (Copiadas do seu r134a_props.py) ---
# Constantes para Pressão de Saturação (P em kPa, T em Kelvin)
A = 24.8033968
B = -335.4048
C = -0.0244075
D = 0.000106511
E = -0.000000138865
F = -106450.0

# Constantes para Entalpia do Líquido Saturado (HL em kJ/kg, T em Celsius)
G = 200.0
H = 1.000000000
I = 0.000000000
J = 0.000000000
K = 0.000000000

# Constantes para Entalpia do Vapor Saturado (HV em kJ/kg, T em Celsius)
L = 397.747352
M = 0.697479704
N = -0.004101890
O = 0.00001022830
P_const = 0.000000009998000

def calcular_pressao_sat(temperatura_kelvin):
    if temperatura_kelvin <= 0:
        raise ValueError("A temperatura em Kelvin deve ser positiva.")
    try:
        ln_P = (A + B / temperatura_kelvin +
                C * math.log(temperatura_kelvin) +
                D * temperatura_kelvin +
                E * temperatura_kelvin**2 +
                F / temperatura_kelvin**2)
        return math.exp(ln_P)
    except OverflowError:
        raise ValueError("Temperatura fora da faixa de aplicabilidade da correlação para pressão.")
    except Exception as e:
        raise RuntimeError(f"Erro no cálculo da pressão: {e}")

def calcular_hl_sat(temperatura_celsius):
    return G + H * temperatura_celsius + I * (temperatura_celsius**2) + J * (temperatura_celsius**3) + K * (temperatura_celsius**4)

def calcular_hv_sat(temperatura_celsius):
    return (L + M * temperatura_celsius + N * (temperatura_celsius**2) +
            O * (temperatura_celsius**3) + P_const * (temperatura_celsius**4))

# --- Rotas do Flask ---

@app.route('/')
def index():
    """Serve a página HTML principal."""
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """Endpoint da API para calcular as propriedades."""
    data = request.get_json()
    if not data or 'temperature' not in data:
        return jsonify({"error": "Temperatura não fornecida."}), 400

    try:
        temperatura_celsius = float(data['temperature'])
        temperatura_kelvin = temperatura_celsius + 273.15

        pressao_kpa = calcular_pressao_sat(temperatura_kelvin)
        hl_kjkg = calcular_hl_sat(temperatura_celsius)
        hv_kjkg = calcular_hv_sat(temperatura_celsius)
        calor_latente = hv_kjkg - hl_kjkg

        return jsonify({
            "pressure": pressao_kpa,
            "hl": hl_kjkg,
            "hv": hv_kjkg,
            "latent_heat": calor_latente
        })

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Erro interno do servidor: {e}"}), 500

if __name__ == '__main__':
    # Para rodar localmente: http://127.0.0.1:5000/
    app.run(debug=True) # debug=True é bom para desenvolvimento, mas desative em produção
