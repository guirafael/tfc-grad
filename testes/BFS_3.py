import wntr
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# CARREGAR MODELO
inp_file = "./dados/base_isolada_v2.inp"
wn = wntr.network.WaterNetworkModel(inp_file)

# CONVERTER PARA GRAFO NÃO DIRECIONADO
G_und = wn.to_graph().to_undirected()

# RAÍZES: reservatório + tanques
raizes = wn.reservoir_name_list + wn.tank_name_list
print(f"Raízes: {raizes}")

# Inicializar estruturas
fila = deque()
node_cluster = {}

# Colocar TODAS as raízes na fila ao mesmo tempo no início
for i, raiz in enumerate(raizes):
  if raiz in G_und:
    node_cluster[raiz] = i + 1 # Define o ID do cluster da raiz
    fila.append(raiz) # Entra na fila de exploração

# Rodar o loop clássico da BFS
while fila:
  no_atual = fila.popleft()
  cluster_atual = node_cluster[no_atual]

  # Olha os vizinhos (nós conectados pelas tubulações)
  for vizinho in G_und.neighbors(no_atual):
    # Se o vizinho ainda não foi visitado por NENHUMA raiz
    if vizinho not in node_cluster:
      node_cluster[vizinho] = cluster_atual # Herda o cluster
      fila.append(vizinho) # Vai para a fila expandir depois

# Resultados
print(f"Nós alocados: {len(node_cluster)}")
print(f"Clusters gerados: {set(node_cluster.values())}")
for c in sorted(set(node_cluster.values())):
  nos = [n for n, v in node_cluster.items() if v == c]
  print(f"  Cluster {c}: {len(nos)} nós")

# PLOTAGEM
wntr.graphics.plot_network(
  wn,
  node_attribute=node_cluster, # Pinta os nós com as cores dos DMCs
  node_size=30, # Aumenta um pouco o nó para você enxergar os clusters
  title="DMCs propostos — BFS multi-fonte"
)

plt.show()