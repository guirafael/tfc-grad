# Este código implementa uma BFS multi-fonte simultâneo para alocar nós a DMCs, considerando todas as raízes (reservatórios e tanques) ao mesmo tempo.
# Ele expande camada por camada a partir de todas as raízes, garantindo que cada nó seja alocado ao cluster da raiz mais próxima.
# O resultado é uma divisão do grafo em clusters conectados, cada um associado a uma raiz específica.
# O código também imprime o número de nós alocados e os clusters gerados, além de plotar a rede com os nós coloridos de acordo com seus clusters.

# A partir desse resultado vamos avaliar se realmente precisamos utilizar todas as raízes ou se podemos filtrar raízes que fazem parte de uma mesma cadeia de abastecimento 
# Isso nos permitirá obter uma divisão mais equilibrada e eficiente da rede.

import wntr
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# CARREGAR MODELO
inp_file = "./dados/base_isolada_v2.inp"
wn = wntr.network.WaterNetworkModel(inp_file)

# CONVERTER PARA GRAFO NÃO DIRECIONADO
G_und = wn.to_graph().to_undirected()

# RAÍZES
raizes = wn.reservoir_name_list + wn.tank_name_list # Aqui pega todas as raízes (reservatórios e tanques)
print(f"Raízes: {raizes}")

# BFS MULTI-FONTE SIMULTÂNEO
node_cluster = {}
fila = deque()

# Inicializar todas as raízes ao mesmo tempo
for i, raiz in enumerate(raizes):
  if raiz in G_und:
    node_cluster[raiz] = i + 1
    fila.append(raiz)

# Expandir camada por camada simultaneamente
while fila:
  no_atual = fila.popleft()
  cluster_atual = node_cluster[no_atual]
  
  for vizinho in G_und.neighbors(no_atual):
    if vizinho not in node_cluster:
      node_cluster[vizinho] = cluster_atual
      fila.append(vizinho)

print(f"Nós alocados: {len(node_cluster)}")
print(f"Clusters gerados: {set(node_cluster.values())}")
for c in sorted(set(node_cluster.values())):
  nos = [n for n, v in node_cluster.items() if v == c]
  print(f"  Cluster {c} (raiz: {raizes[c-1]}): {len(nos)} nós")

# PLOTAR
wntr.graphics.plot_network(
  wn,
  node_attribute=node_cluster,
  node_size=15,
  title="DMCs propostos — BFS multi-fonte simultâneo"
)

plt.show()