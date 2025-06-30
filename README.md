# dadosR134a
# Propriedades Termodinâmicas do R134a

Este repositório contém um script em Python para calcular as propriedades de saturação (Pressão, Entalpia do Líquido Saturado e Entalpia do Vapor Saturado) para o refrigerante R134a. As correlações utilizadas são baseadas em um script FORTRAN legado, garantindo a consistência com os métodos de cálculo existentes.

## Funcionalidades

* Cálculo da Pressão de Saturação (P) em kPa.
* Cálculo da Entalpia do Líquido Saturado (HL) em kJ/kg.
* Cálculo da Entalpia do Vapor Saturado (HV) em kJ/kg.
* Interação simples via linha de comando: o usuário informa a temperatura de saturação em Celsius.

## Como Usar

Siga os passos abaixo para baixar e executar o script na sua máquina.

### Pré-requisitos

Você precisará ter o Python instalado em seu sistema. Versões 3.6 ou superiores são recomendadas.

* [Download Python](https://www.python.org/downloads/)

### Instalação e Execução

1.  **Clone o Repositório:**
    Abra seu terminal ou prompt de comando e clone este repositório para sua máquina local:

    ```bash
    git clone [https://github.com/SEU_USUARIO_GITHUB/termodinamica_r134a.git](https://github.com/SEU_USUARIO_GITHUB/termodinamica_r134a.git)
    cd termodinamica_r134a
    ```
    *(**Importante**: Substitua `SEU_USUARIO_GITHUB` pelo seu nome de usuário real no GitHub.)*

2.  **Execute o Script:**
    Com o terminal ainda no diretório `termodinamica_r134a`, execute o script Python:

    ```bash
    python r134a_props.py
    ```

3.  **Interação:**
    O programa solicitará que você digite a temperatura de saturação em Celsius. Digite um valor numérico e pressione `Enter`. Para sair do programa, digite `q` e pressione `Enter`.

    Exemplo de interação:
    ```
    --------------------------------------------------
     Calculadora de Propriedades de Saturação do R134a
    --------------------------------------------------
    Baseado em correlações de script FORTRAN.
    Entre com a temperatura de saturação em Celsius.
    As propriedades serão retornadas em:
      - Pressão: kPa
      - Entalpias (HL e HV): kJ/kg
    --------------------------------------------------

    Digite a temperatura de saturação em Celsius (ou 'q' para sair): 25

    --- Resultados para T = 25.00 °C ---
      Pressão de Saturação (P): 662.6685 kPa
      Entalpia Líquido Saturado (HL): 225.0000 kJ/kg
      Entalpia Vapor Saturado (HV): 409.8436 kJ/kg
      Calor Latente de Vaporização (HV-HL): 184.8436 kJ/kg

    Digite a temperatura de saturação em Celsius (ou 'q' para sair): q
    Saindo do programa. Até mais!
    ```

## Como Contribuir

Se você encontrar algum problema ou tiver sugestões de melhoria, sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` (se você criar um) para mais detalhes.

---
