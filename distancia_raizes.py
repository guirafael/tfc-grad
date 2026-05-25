# Este script calcula a distância topológica (número de arestas) entre todas as raízes (reservatórios e tanques) do modelo hidráulico, usando o grafo não direcionado da rede.
# Ele utiliza a função `shortest_path_length` do NetworkX para obter a distância entre cada par de raízes.
# Se não houver caminho entre elas, é indicado que estão desconectadas.

# Podemos utilizar essa informação para entender a estrutura da rede e avaliar a proximidade entre as raízes.
# Isso pode ser útil para considerar ou não uma raiz como nó inicial para o algoritmo de clusterização, ou para avaliar a necessidade de criar clusters separados para raízes muito distantes entre si.

import wntr
import networkx as nx

# CARREGAR MODELO
inp_file = "./dados/base_isolada_v2.inp"
wn = wntr.network.WaterNetworkModel(inp_file)

# CONVERTER PARA GRAFO NÃO DIRECIONADO
G_und = wn.to_graph().to_undirected()

# RAÍZES
raizes = wn.reservoir_name_list + wn.tank_name_list
print(f"Raízes: {raizes}")

# DISTÂNCIA TOPOLÓGICA ENTRE TODAS AS RAÍZES
for r1 in raizes:
  for r2 in raizes:
    if r1 != r2:
      try:
        dist = nx.shortest_path_length(G_und, r1, r2)
        print(f"  {r1} → {r2}: {dist} arestas")
      except:
        print(f"  {r1} → {r2}: sem caminho")