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
    """
    Calcula a pressão de saturação do R134a.
    Baseado na correlação do script FORTRAN.

    Args:
        temperatura_kelvin (float): Temperatura de saturação em Kelvin.

    Returns:
        float: Pressão de saturação em kPa.
    """
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
    """
    Calcula a entalpia do líquido saturado do R134a.
    Baseado na correlação polinomial do script FORTRAN.

    Args:
        temperatura_celsius (float): Temperatura de saturação em Celsius.

    Returns:
        float: Entalpia do líquido saturado em kJ/kg.
    """
    # Para as constantes G, H, I, J, K, o script FORTRAN mostra I, J, K como zero.
    # Se essa é a intenção, a equação simplifica para HL = G + H*T.
    return G + H * temperatura_celsius + I * (temperatura_celsius**2) + J * (temperatura_celsius**3) + K * (temperatura_celsius**4)

def calcular_hv_sat(temperatura_celsius):
    """
    Calcula a entalpia do vapor saturado do R134a.
    Baseado na correlação polinomial do script FORTRAN.

    Args:
        temperatura_celsius (float): Temperatura de saturação em Celsius.

    Returns:
        float: Entalpia do vapor saturado em kJ/kg.
    """
    return (L + M * temperatura_celsius + N * (temperatura_celsius**2) +
            O * (temperatura_celsius**3) + P_const * (temperatura_celsius**4))

if __name__ == "__main__":
    print("--------------------------------------------------")
    print(" Calculadora de Propriedades de Saturação do R134a")
    print("--------------------------------------------------")
    print("Baseado em correlações de script FORTRAN.")
    print("Entre com a temperatura de saturação em Celsius.")
    print("As propriedades serão retornadas em: ")
    print("  - Pressão: kPa")
    print("  - Entalpias (HL e HV): kJ/kg")
    print("--------------------------------------------------")

    while True:
        try:
            temp_input_str = input("\nDigite a temperatura de saturação em Celsius (ou 'q' para sair): ")

            if temp_input_str.lower() == 'q':
                print("Saindo do programa. Até mais!")
                break

            temperatura_celsius = float(temp_input_str)
            temperatura_kelvin = temperatura_celsius + 273.15

            # Verifica um range razoável para o R134a
            if not (-40 <= temperatura_celsius <= 100): # Exemplo de range comum para R134a
                print("Atenção: A temperatura fornecida está fora de um range comum para R134a (-40 a 100 °C).")
                print("Os resultados podem não ser precisos fora deste intervalo.")


            pressao_kpa = calcular_pressao_sat(temperatura_kelvin)
            hl_kjkg = calcular_hl_sat(temperatura_celsius)
            hv_kjkg = calcular_hv_sat(temperatura_celsius)

            print(f"\n--- Resultados para T = {temperatura_celsius:.2f} °C ---")
            print(f"  Pressão de Saturação (P): {pressao_kpa:.4f} kPa")
            print(f"  Entalpia Líquido Saturado (HL): {hl_kjkg:.4f} kJ/kg")
            print(f"  Entalpia Vapor Saturado (HV): {hv_kjkg:.4f} kJ/kg")
            print(f"  Calor Latente de Vaporização (HV-HL): {(hv_kjkg - hl_kjkg):.4f} kJ/kg")

        except ValueError as ve:
            print(f"Erro de entrada: {ve}. Por favor, digite um número válido.")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
