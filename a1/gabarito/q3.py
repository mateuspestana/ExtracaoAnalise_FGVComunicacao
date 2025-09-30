# Questão 3 - Análise de Perfis de Influenciadores com PCA e K-Means
# Objetivo: criar um pipeline simples com pandas, numpy, sklearn, matplotlib e seaborn
# Passos:
# 1) Criar a base de dados (igual à prova)
# 2) EDA por plataforma (médias)
# 3) Padronização dos dados numéricos
# 4) PCA com 2 componentes
# 5) K-Means com 4 clusters
# 6) Caracterização dos clusters e pequenas interpretações

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração visual simples
plt.style.use('default')
sns.set_palette("viridis")

# ===============
# Base de dados
# ===============
np.random.seed(2024)

plataformas = ['Instagram', 'TikTok', 'YouTube', 'Twitter', 'LinkedIn']
n_influencers_por_plataforma = [50, 45, 35, 30, 20]

lista_plataformas = []
for plataforma, n in zip(plataformas, n_influencers_por_plataforma):
    lista_plataformas.extend([plataforma] * n)

total_influencers = len(lista_plataformas)

engajamento_base = {'Instagram': 3.2, 'TikTok': 5.8, 'YouTube': 2.1, 'Twitter': 1.8, 'LinkedIn': 4.5}
posts_base = {'Instagram': 6, 'TikTok': 12, 'YouTube': 2, 'Twitter': 15, 'LinkedIn': 4}
autenticidade_base = {'Instagram': 6.5, 'TikTok': 7.8, 'YouTube': 8.2, 'Twitter': 7.0, 'LinkedIn': 8.5}

df_influencers = pd.DataFrame({
    'PlataformaPrincipal': lista_plataformas,
    'NomeInfluencer': [f'@creator_{i+1:03d}' for i in range(total_influencers)],
})

df_influencers['TaxaEngajamento'] = [np.random.normal(engajamento_base[plat], 1.2) for plat in df_influencers['PlataformaPrincipal']]
df_influencers['PostsPorSemana'] = [np.random.normal(posts_base[plat], 3) for plat in df_influencers['PlataformaPrincipal']]
df_influencers['PontuacaoAutenticidade'] = [np.random.normal(autenticidade_base[plat], 1.5) for plat in df_influencers['PlataformaPrincipal']]
df_influencers['DiversidadeConteudo'] = np.random.normal(6.5, 2.0, total_influencers)
df_influencers['IndiceConversao'] = np.random.normal(25, 15, total_influencers)

# Ajustes para manter valores realistas
df_influencers['TaxaEngajamento'] = np.clip(df_influencers['TaxaEngajamento'], 0.5, 12.0).round(1)
df_influencers['PostsPorSemana'] = np.clip(df_influencers['PostsPorSemana'], 1, 25).astype(int)
df_influencers['DiversidadeConteudo'] = np.clip(df_influencers['DiversidadeConteudo'], 1, 10).round(1)
df_influencers['PontuacaoAutenticidade'] = np.clip(df_influencers['PontuacaoAutenticidade'], 1, 10).round(1)
df_influencers['IndiceConversao'] = np.clip(df_influencers['IndiceConversao'], 5, 80).astype(int)

print("-- Base de influenciadores criada!")
print(f"Total: {len(df_influencers)} influenciadores")
print(df_influencers.head())

# =============================
# Etapa 1: EDA por plataforma
# =============================
print("\n=== Etapa 1: Análise descritiva por plataforma ===")
cols_numericas = [
    'TaxaEngajamento', 'PostsPorSemana', 'DiversidadeConteudo',
    'PontuacaoAutenticidade', 'IndiceConversao'
]

grp = df_influencers.groupby('PlataformaPrincipal')[cols_numericas].mean().round(2)
print(grp)

# Alguns insights simples (automáticos)
print("\nAlguns insights:")
print("- Plataforma com maior engajamento médio:", grp['TaxaEngajamento'].idxmax(), grp['TaxaEngajamento'].max())
print("- Plataforma com mais posts por semana:", grp['PostsPorSemana'].idxmax(), grp['PostsPorSemana'].max())
print("- Plataforma com maior autenticidade média:", grp['PontuacaoAutenticidade'].idxmax(), grp['PontuacaoAutenticidade'].max())

# =====================================
# Etapa 2: Padronização (StandardScaler)
# =====================================
print("\n=== Etapa 2: Padronização dos dados ===")
print("Antes (amostra):")
print(df_influencers[cols_numericas].head())

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_influencers[cols_numericas])

print("Depois (amostra):")
print(pd.DataFrame(X_scaled, columns=cols_numericas).head())

# =========================
# Etapa 3: PCA (2 comp.)
# =========================
print("\n=== Etapa 3: PCA com 2 componentes ===")
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_scaled)

var_total = pca.explained_variance_ratio_.sum()
print(f"Variância total explicada (PC1 + PC2): {var_total:.2f}")
print("Componentes (loadings):")
loadings = pd.DataFrame(pca.components_, columns=cols_numericas, index=['PC1', 'PC2']).round(2)
print(loadings)

# DataFrame com PCs (para plot e clustering)
df_pca = pd.DataFrame(X_pca, columns=['PC1', 'PC2'])

# ===========================
# Etapa 4: K-Means (k = 4)
# ===========================
print("\n=== Etapa 4: K-Means com k=4 ===")
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
clusters = kmeans.fit_predict(df_pca)

df_resultado = df_influencers.copy()
df_resultado['PC1'] = df_pca['PC1']
df_resultado['PC2'] = df_pca['PC2']
df_resultado['cluster'] = clusters

print("Centróides (no espaço dos PCs):")
print(pd.DataFrame(kmeans.cluster_centers_, columns=['PC1','PC2']).round(2))

# Gráfico simples dos clusters
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df_resultado, x='PC1', y='PC2', hue='cluster', palette='viridis', s=50)
plt.title('K-Means (k=4) nos 2 PCs')
plt.legend(title='cluster')
plt.tight_layout()
plt.show()

# =====================================
# Etapa 5: Caracterização dos clusters
# =====================================
print("\n=== Etapa 5: Caracterização dos clusters ===")
caracteristicas = df_resultado.groupby('cluster')[cols_numericas].mean().round(2)
print("Médias por cluster (nas variáveis originais):")
print(caracteristicas)

# Também é legal ver a distribuição de plataformas por cluster
print("\nDistribuição de plataformas por cluster:")
print(df_resultado.groupby(['cluster','PlataformaPrincipal']).size().unstack(fill_value=0))

# Nomeando arquétipos (regra bem simples, estilo júnior):
# Vamos usar thresholds com base nas médias gerais para dar nomes sugestivos.
medias_globais = df_influencers[cols_numericas].mean()
nomes_clusters = {}
for c in sorted(df_resultado['cluster'].unique()):
    linha = caracteristicas.loc[c]
    nome = []
    if linha['PostsPorSemana'] > medias_globais['PostsPorSemana']:
        nome.append('Alta Frequência')
    if linha['TaxaEngajamento'] > medias_globais['TaxaEngajamento']:
        nome.append('Engajados')
    if linha['PontuacaoAutenticidade'] > medias_globais['PontuacaoAutenticidade']:
        nome.append('Autênticos')
    if linha['IndiceConversao'] > medias_globais['IndiceConversao']:
        nome.append('Conversores')
    if len(nome) == 0:
        nome = ['Equilibrados']
    nomes_clusters[c] = " / ".join(nome)

print("\nSugestão de nomes para os arquétipos:")
for c, n in nomes_clusters.items():
    print(f"- Cluster {c}: {n}")

# Interpretação curta (exemplo simples)
print("\nInterpretação (exemplo):")
print("- PC1 e PC2 parecem combinar engajamento, frequência e autenticidade em direções diferentes.")
print("- Os clusters mostram grupos com perfis distintos (ex.: mais posts e engajamento, ou mais conversão).")
print("- Uma marca pode escolher clusters com mais 'Engajados' para awareness ou 'Conversores' para performance.")
