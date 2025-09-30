# # Questão 6 – EXTRA – Raspagem (0,5 ponto)

# No site oficial de documentação da API do Scikit-learn (https://scikit-learn.org/stable/api/index.html), observe que:
# - Na **barra lateral esquerda**, encontram-se listados os módulos principais (sklearn, sklearn.base, sklearn.calibration, sklearn.cluster, sklearn.compose, ...).
# - Dentro de cada módulo, a documentação exibe as funções e classes disponíveis.
# Exemplo: no módulo `sklearn.tree`, aparecem `DecisionTreeClassifier, DecisionTreeRegressor, ExtraTreeClassifier, ExtraTreeRegressor, export_graphviz, export_text, plot_tree`.

# Suponha que desejamos fazer raspagem de dados nesse site para coletar:

# 1.	A lista de todos os módulos (apenas os nomes dos módulos);
# 2.	A lista de todas as funções/classes (apenas os nomes das funções/classes).

# Sabemos que cada lista pode ser obtida identificando corretamente a tag HTML e a classe CSS utilizadas na página para representar esses elementos. No exemplo:

# ```html
# <h1 class='heading-1'>Documentação</h1>
# ```
# a tag é `h1` e a classe é `heading-1`.

# Indique, separadamente, qual é a combinação (tag + classe) que retorna somente os módulos e qual retorna somente as funções/classes.

# Responda no formato:

# ```python
# {'categoria': 'modulos', 'tag': 'XXX', 'classe': 'YYY'}
# {'categoria': 'funcoes/classes', 'tag': 'AAA', 'classe': 'BBB'}

{'categoria': 'modulos', 'tag': 'li', 'classe': 'toctree-l1'}
{'categoria': 'funcoes/classes', 'tag': 'li', 'classe': 'toctree-l2'}