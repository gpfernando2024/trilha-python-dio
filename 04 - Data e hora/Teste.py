def analise_vendas(vendas):
    # Calcular o total de vendas
    total_vendas = sum(vendas)
    # Calcular a média mensal de vendas
    media_vendas = total_vendas / len(vendas)
   # Retorna o total de vendas e a média mensal formatada com duas casas decimais
    return f"{total_vendas}, {media_vendas:.2f}"

def obter_entrada_vendas():
    # Solicita a entrada do usuário para as vendas de cada mês
    entrada = input("Digite as vendas de cada mês separadas por vírgula: ")
    # Converte a entrada em uma lista de inteiros
    vendas = list(map(int, entrada.split(',')))
    return vendas

# Executa as funções
vendas = obter_entrada_vendas()
print(analise_vendas(vendas))