# Questão 5 - Sistema de Análise de Notas Escolares
# Objetivo: calcular médias, classificar status, analisar por turma e gerar relatório de alunos em risco.

import pandas as pd
import numpy as np

# ==========================
# Base de dados (da prova)
# ==========================
np.random.seed(123)

alunos_data = {
    'nome': ['Ana S.', 'Bruno C.', 'Carla S.', 'Diego O.', 'Elena R.',
             'Felipe L.', 'Gabriela S.', 'Henrique A.', 'Isabela F.', 'João P.',
             'Larissa M.', 'Marcos V.', 'Natália C.', 'Otávio R.', 'Patrícia G.',
             'Rafael B.', 'Sofia R.', 'Thiago N.', 'Vitória C.', 'Wellington T.'],
    'turma': ['A', 'A', 'B', 'A', 'B', 'C', 'B', 'C', 'A', 'B',
              'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C'],
    'matematica': [8.5, 7.2, 9.1, 6.8, 8.9, 7.5, 8.0, 6.3, 9.5, 7.8,
                   8.2, 6.9, 8.7, 7.1, 9.0, 7.6, 8.4, 6.5, 8.8, 7.3],
    'portugues': [9.0, 6.8, 8.5, 7.2, 9.2, 6.9, 8.1, 7.4, 9.3, 8.0,
                  7.7, 7.0, 8.9, 6.6, 8.8, 7.5, 8.3, 6.8, 9.1, 7.2],
    'ciencias': [7.8, 8.1, 9.0, 7.5, 8.6, 7.9, 8.3, 7.0, 9.2, 8.4,
                 8.0, 7.6, 8.5, 7.3, 8.9, 8.2, 8.1, 7.1, 8.7, 7.8],
    'faltas': [2, 8, 1, 12, 3, 15, 4, 18, 0, 6,
               5, 14, 2, 16, 1, 7, 3, 13, 2, 9]
}

df_notas = pd.DataFrame(alunos_data)
print("📚 Base de notas criada!")
print(f"Total de alunos: {len(df_notas)}")
print(df_notas.head())

# ==============================
# Item A: Média geral por aluno
# ==============================
print("\n=== Item A: Média geral ===")
# A1: média aritmética das 3 disciplinas
cols = ['matematica', 'portugues', 'ciencias']
df_notas['media_geral'] = df_notas[cols].mean(axis=1).round(2)

# A2: maior e menor média
idx_maior = df_notas['media_geral'].idxmax()
idx_menor = df_notas['media_geral'].idxmin()
print("Maior média:", df_notas.loc[idx_maior, 'nome'], df_notas.loc[idx_maior, 'media_geral'])
print("Menor média:", df_notas.loc[idx_menor, 'nome'], df_notas.loc[idx_menor, 'media_geral'])

# ==================================
# Item B: Classificação por Status
# ==================================
print("\n=== Item B: Status ===")

def classificar_status(media, faltas):
    # Regras da prova (em ordem simples)
    if (media >= 7.0) and (faltas <= 10):
        return "Aprovado"
    elif (media >= 6.0) and (media < 7.0) and (faltas <= 15):
        return "Recuperação"
    else:
        return "Reprovado"

# Aplicando função linha a linha
df_notas['status'] = df_notas.apply(lambda r: classificar_status(r['media_geral'], r['faltas']), axis=1)

# B2: contagem por status
contagem_status = df_notas['status'].value_counts()
print("Contagem por status:")
print(contagem_status)

# ========================
# Item C: Por Turma
# ========================
print("\n=== Item C: Análise por Turma ===")
agr_turma = df_notas.groupby('turma').agg(
    media_geral_turma=('media_geral', 'mean'),
    total_alunos=('nome', 'count'),
    aprovados=('status', lambda s: (s == 'Aprovado').sum()),
    faltas_medias=('faltas', 'mean')
).round(2)
print(agr_turma)

melhor_turma = agr_turma['media_geral_turma'].idxmax()
print("Turma com melhor desempenho:", melhor_turma)

# ========================
# Item D: Relatório em risco
# ========================
print("\n=== Item D: Alunos em risco ===")
risco = df_notas[df_notas['status'].isin(['Reprovado', 'Recuperação'])].copy()
colunas_rel = ['nome', 'turma', 'media_geral', 'faltas', 'status']
relatorio_risco = risco[colunas_rel].sort_values('media_geral')
print(relatorio_risco)

# Interpretação final simples
print("\nInterpretação final (exemplo):")
print(f"- Melhor turma: {melhor_turma}.")
print(f"- Alunos que precisam de atenção: {len(relatorio_risco)}.")
# Observação simples sobre faltas e desempenho
correlacao_faltas_media = round(df_notas[['faltas', 'media_geral']].corr().loc['faltas', 'media_geral'], 2)
print(f"- Correlação (faltas x média_geral): {correlacao_faltas_media}")
