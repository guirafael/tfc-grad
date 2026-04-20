import matplotlib.pyplot as mp
import wntr

# CARREGAR MODELO
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
inp_file = os.path.join(BASE_DIR, '..', 'dados', 'base_completa_v6.inp')

wn = wntr.network.WaterNetworkModel(inp_file)

# TRANSFORMAR EM GRAFO
G = wn.to_graph()

# EXEMPLO DE CLUSTERIZAÇÃO
from networkx.algorithms import community

communities = community.greedy_modularity_communities(G)
for i, c in enumerate(communities):
  print(f"Cluster {i}: {len(c)} nós")

# PLOTAR A REDE
node_cluster = {}
for i, comm in enumerate(communities):
  for node in comm:
    node_cluster[node] = i

wntr.graphics.plot_network(
  wn,
  node_attribute=node_cluster,
  node_size=10,
  title="Clusters - Greedy Modularity"
)

mp.show()