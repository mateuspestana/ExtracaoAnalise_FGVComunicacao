# Questão 4 - Análise de Dados de E-commerce
# Objetivo: executar os itens A, B e C com pandas e numpy, com comentários simples.

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ==========================
# Base de dados (da prova)
# ==========================
np.random.seed(42)

n_vendas = 800
categorias = ['Eletrônicos', 'Roupas', 'Casa', 'Livros', 'Esporte']
canais = ['Online', 'Loja Física', 'App Mobile', 'Telefone']
cidades = ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Curitiba', 'Salvador']

df_vendas = pd.DataFrame({
    'id_venda': range(1, n_vendas + 1),
    'categoria_produto': np.random.choice(categorias, n_vendas),
    'canal_venda': np.random.choice(canais, n_vendas),
    'cidade': np.random.choice(cidades, n_vendas),
    'qtd_vendida': np.random.randint(1, 10, n_vendas),
    'preco_unit': np.round(np.random.normal(150, 80, n_vendas), 2),
    'data_venda': [datetime(2024, 1, 1) + timedelta(days=int(x)) for x in np.random.randint(0, 365, n_vendas)],
    'satisfacao_cliente': np.round(np.random.normal(4.2, 0.8, n_vendas), 1),
    'tempo_entrega': np.random.randint(1, 15, n_vendas)
})

# Ajustes
df_vendas['preco_unit'] = df_vendas['preco_unit'].clip(10, 500)
df_vendas['satisfacao_cliente'] = df_vendas['satisfacao_cliente'].clip(1.0, 5.0)

# Valor total
df_vendas['valor_total'] = df_vendas['qtd_vendida'] * df_vendas['preco_unit']

# Valores ausentes em satisfacao_cliente
mask_nan = np.random.choice([True, False], size=len(df_vendas), p=[0.03, 0.97])
df_vendas.loc[mask_nan, 'satisfacao_cliente'] = np.nan

print("📦 Base de vendas criada!")
print(f"Total de registros: {len(df_vendas)}")
print(df_vendas.head())

# ===============================
# Item A: Limpeza e Preparação
# ===============================
print("\n=== Item A: Limpeza e Preparação ===")

# A1: Quantos valores ausentes em satisfacao_cliente
faltando = df_vendas['satisfacao_cliente'].isna().sum()
print("A1 - Valores ausentes em satisfacao_cliente:", faltando)

# A2: Preencher NaN com mediana por categoria
medianas_por_cat = df_vendas.groupby('categoria_produto')['satisfacao_cliente'].median()
# Usando transform para replicar a mediana da categoria em cada linha
medianas_por_cat_map = df_vendas['categoria_produto'].map(medianas_por_cat)
df_vendas['satisfacao_cliente'] = df_vendas['satisfacao_cliente'].fillna(medianas_por_cat_map)

# A3: Renomear colunas para inglês
renomear = {
    'categoria_produto': 'product_category',
    'canal_venda': 'sales_channel',
    'qtd_vendida': 'quantity_sold',
    'preco_unit': 'unit_price',
    'data_venda': 'sale_date',
    'satisfacao_cliente': 'customer_satisfaction',
    'tempo_entrega': 'delivery_time'
}
df = df_vendas.rename(columns=renomear).copy()

print("Colunas após renomear:")
print(df.columns.tolist())

# ==============================================
# Item B: Análise por Categoria de Produto
# ==============================================
print("\n=== Item B: Análise por Categoria ===")

# B1: Métricas por categoria
agr = df.groupby('product_category').agg(
    total_vendas=('id_venda', 'count'),
    valor_total_vendido=('valor_total', 'sum'),
    ticket_medio=('valor_total', 'mean'),
    satisfacao_media=('customer_satisfaction', 'mean'),
    tempo_medio_entrega=('delivery_time', 'mean')
).round(2)
print(agr)

# B2: Ordenar pelo valor total vendido
agr_ordenado = agr.sort_values('valor_total_vendido', ascending=False)
print("\nOrdenado por valor_total_vendido (desc):")
print(agr_ordenado)

# B3: Melhor e pior satisfação
melhor_cat = agr['satisfacao_media'].idxmax()
pior_cat = agr['satisfacao_media'].idxmin()
print(f"\nMelhor satisfação: {melhor_cat} -> {agr.loc[melhor_cat, 'satisfacao_media']:.2f}")
print(f"Pior satisfação: {pior_cat} -> {agr.loc[pior_cat, 'satisfacao_media']:.2f}")

print("\nInsights rápidos (exemplo):")
print("- Categoria com maior receita ajuda a priorizar campanhas de marketing.")
print("- Ticket médio mostra onde clientes gastam mais por compra.")
print("- Satisfação e entrega podem indicar foco em melhoria operacional.")

# ======================================
# Item C: Análise por Canal e Filtros
# ======================================
print("\n=== Item C: Canal e Filtros ===")

# C1: Tabela pivot (sales_channel x product_category) com soma de valor_total
pivot = pd.pivot_table(
    df,
    index='sales_channel',
    columns='product_category',
    values='valor_total',
    aggfunc='sum',
    fill_value=0
)
print("Tabela pivot (soma de valor_total):")
print(pivot)

# C2: Filtro premium
filtro = (
    (df['valor_total'] > 200) &
    (df['customer_satisfaction'] >= 4.0) &
    (df['delivery_time'] <= 7)
)
df_premium = df.loc[filtro].copy()

# C3: Colunas selecionadas
colunas_c3 = ['id_venda', 'product_category', 'sales_channel', 'valor_total', 'customer_satisfaction']
resultado_c3 = df_premium[colunas_c3]
print("\nVendas premium (amostra):")
print(resultado_c3.head())

# Perguntas de interpretação
canal_melhor = pivot.sum(axis=1).idxmax()
qtd_premium = len(resultado_c3)
print(f"\nCanal com melhor desempenho (soma receita): {canal_melhor}")
print(f"Quantidade de vendas premium: {qtd_premium}")

print("\nComo isso ajuda a empresa?")
print("- Focar no canal com maior receita para campanhas.")
print("- Usar vendas premium para entender perfil de clientes de alto valor.")
