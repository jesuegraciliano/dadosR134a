import tkinter as tk
from tkinter import ttk
import math

# Constantes para as correlações do R134a (extraídas do script FORTRAN)
# Baseado em T em Kelvin para Pressão, e T em Celsius para HL e HV.

# Constantes para Pressão de Saturação (P em kPa, T em Kelvin)
# ln(P) = A + B/T + C*ln(T) + D*T + E*T**2 + F/T**2
A = 24.8033968
B = -335.4048
C = -0.0244075
D = 0.000106511
E = -0.000000138865
F = -106450.0

# Constantes para Entalpia do Líquido Saturado (HL em kJ/kg, T em Celsius)
# HL = G + H*T + I*T**2 + J*T**3 + K*T**4
G = 200.0
H = 1.000000000
I = 0.000000000
J = 0.000000000
K = 0.000000000

# Constantes para Entalpia do Vapor Saturado (HV em kJ/kg, T em Celsius)
# HV = L + M*T + N*T**2 + O*T**3 + P_const*T**4
L = 397.747352
M = 0.697479704
N = -0.004101890
O = 0.00001022830
P_const = 0.000000009998000 # Renomeado para P_const para evitar conflito com 'P' de Pressão

def calcular_pressao_sat(temperatura_kelvin):
    """Calcula a pressão de saturação."""
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
    """Calcula a entalpia do líquido saturado."""
    return G + H * temperatura_celsius + I * (temperatura_celsius**2) + J * (temperatura_celsius**3) + K * (temperatura_celsius**4)

def calcular_hv_sat(temperatura_celsius):
    """Calcula a entalpia do vapor saturado."""
    return (L + M * temperatura_celsius + N * (temperatura_celsius**2) +
            O * (temperatura_celsius**3) + P_const * (temperatura_celsius**4))

def calcular_propriedades():
    """Função para calcular e exibir as propriedades."""
    try:
        temp_celsius_str = temp_entry.get()
        temperatura_celsius = float(temp_celsius_str)
        temperatura_kelvin = temperatura_celsius + 273.15

        if not (-40 <= temperatura_celsius <= 100):
            resultado_pressao.config(text="Atenção: Temperatura fora do range comum.")
            resultado_hl.config(text="")
            resultado_hv.config(text="")
            resultado_calor_latente.config(text="")
            return

        pressao_kpa = calcular_pressao_sat(temperatura_kelvin)
        hl_kjkg = calcular_hl_sat(temperatura_celsius)
        hv_kjkg = calcular_hv_sat(temperatura_celsius)
        calor_latente = hv_kjkg - hl_kjkg

        resultado_pressao.config(text=f"{pressao_kpa:.4f} kPa")
        resultado_hl.config(text=f"{hl_kjkg:.4f} kJ/kg")
        resultado_hv.config(text=f"{hv_kjkg:.4f} kJ/kg")
        resultado_calor_latente.config(text=f"{calor_latente:.4f} kJ/kg")

    except ValueError:
        resultado_pressao.config(text="Erro: Digite um número válido.")
        resultado_hl.config(text="")
        resultado_hv.config(text="")
        resultado_calor_latente.config(text="")
    except Exception as e:
        resultado_pressao.config(text=f"Erro: {e}")
        resultado_hl.config(text="")
        resultado_hv.config(text="")
        resultado_calor_latente.config(text="")

# Configuração da janela principal
root = tk.Tk()
root.title("Propriedades de Saturação do R134a")

# Estilo para widgets (opcional)
style = ttk.Style()
style.theme_use('clam')

# Frame principal
main_frame = ttk.Frame(root, padding="12 12 12 12")
main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Label e Entry para Temperatura
temp_label = ttk.Label(main_frame, text="Temperatura de Saturação (°C):")
temp_label.grid(column=0, row=0, sticky=(tk.W, tk.E))
temp_entry = ttk.Entry(main_frame)
temp_entry.grid(column=1, row=0, sticky=(tk.W, tk.E))

# Botão de Calcular
calcular_button = ttk.Button(main_frame, text="Calcular", command=calcular_propriedades)
calcular_button.grid(column=0, row=1, columnspan=2, pady=10)

# Labels para Resultados
pressao_label = ttk.Label(main_frame, text="Pressão de Saturação:")
pressao_label.grid(column=0, row=2, sticky=tk.W)
resultado_pressao = ttk.Label(main_frame, text="")
resultado_pressao.grid(column=1, row=2, sticky=tk.E)

hl_label = ttk.Label(main_frame, text="Entalpia Líquido Saturado (HL):")
hl_label.grid(column=0, row=3, sticky=tk.W)
resultado_hl = ttk.Label(main_frame, text="")
resultado_hl.grid(column=1, row=3, sticky=tk.E)

hv_label = ttk.Label(main_frame, text="Entalpia Vapor Saturado (HV):")
hv_label.grid(column=0, row=4, sticky=tk.W)
resultado_hv = ttk.Label(main_frame, text="")
resultado_hv.grid(column=1, row=4, sticky=tk.E)

calor_latente_label = ttk.Label(main_frame, text="Calor Latente de Vaporização:")
calor_latente_label.grid(column=0, row=5, sticky=tk.W)
resultado_calor_latente = ttk.Label(main_frame, text="")
resultado_calor_latente.grid(column=1, row=5, sticky=tk.E)

# Adiciona um pouco de padding aos widgets
for child in main_frame.winfo_children():
    child.grid_configure(padx=5, pady=5)

# Permite que ao pressionar Enter no campo de temperatura, o cálculo seja feito
root.bind('<Return>', lambda event=None: calcular_button.invoke())
temp_entry.focus() # Coloca o foco inicial no campo de temperatura

root.mainloop()
