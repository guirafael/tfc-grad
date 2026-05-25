# Assim como 'BFS_todas_raizes.py', este código implementa uma BFS multi-fonte simultâneo para alocar nós a DMCs, considerando apenas os tanques como raízes.
# Ele expande camada por camada a partir das raízes, garantindo que cada nó seja alocado ao cluster da raiz mais próxima.
# O resultado é uma divisão do grafo em clusters conectados, cada um associado a uma raiz específica.
# O código também imprime o número de nós alocados e os clusters gerados, além de plotar a rede com os nós coloridos de acordo com seus clusters.

import wntr
import matplotlib.pyplot as plt
from collections import deque

# CARREGAR MODELO
inp_file = "./dados/base_isolada_v2.inp"
wn = wntr.network.WaterNetworkModel(inp_file)

# CONVERTER PARA GRAFO NÃO DIRECIONADO
G_und = wn.to_graph().to_undirected()

# RAÍZES
raizes_dmcs = ['T6698', 'T6701', 'T6702'] # Apenas os tanques como raízes
print(f"Raízes dos DMCs: {raizes_dmcs}")

node_cluster = {}
fila = deque()

for i, raiz in enumerate(raizes_dmcs):
  node_cluster[raiz] = i + 1
  fila.append(raiz)

while fila:
  no_atual = fila.popleft()
  cluster_atual = node_cluster[no_atual]
  for vizinho in G_und.neighbors(no_atual):
    if vizinho not in node_cluster:
      node_cluster[vizinho] = cluster_atual
      fila.append(vizinho)

print(f"Clusters gerados: {set(node_cluster.values())}")
for c in sorted(set(node_cluster.values())):
  nos = [n for n, v in node_cluster.items() if v == c]
  print(f"  Cluster {c} (raiz: {raizes_dmcs[c-1]}): {len(nos)} nós")

wntr.graphics.plot_network(
  wn,
  node_attribute=node_cluster,
  node_size=15,
  title="DMCs propostos — BFS multi-fonte (3 tanques)"
)

plt.show()