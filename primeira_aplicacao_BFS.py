# Esta aplicação tem o objetivo de testar a aplicação do algoritmo BFS (Busca em Largura) para delimitar setores de controle (DMCs) em uma rede de abastecimento de água. 
# A ideia é verificar se o BFS consegue alcançar todos os nós do setor isolado, ou se há nós desconexos.
# Primeiramente, vamos testar com o grafo dirigido (respeitando o sentido do fluxo) e depois com o grafo não dirigido (ignorando o sentido do fluxo).

import wntr
import networkx as nx

# CARREGAR MODELO ISOLADO
inp_file = './dados/base_isolada_v2.inp'
wn = wntr.network.WaterNetworkModel(inp_file)

# CONVERTER EM GRAFO
G = wn.to_graph()

# EXECUTAR BFS A PARTIR DO RESERVATÓRIO E ALOCAR NÓS EM CLUSTER ÚNICO

# TENTATIVA 1: GRAFO DIRIGIDO → BFS SEGUE O SENTIDO DO FLUXO

reservatorio = wn.reservoir_name_list[0]
print(f"Reservatório raiz: {reservatorio}")

# BFS - árvore de abrangência
bfs_tree = nx.bfs_tree(G, source=reservatorio)

# MAPEAR NÓ → CLUSTER (por enquanto temos 1 fonte, então todos ficam no cluster 1)
node_cluster = {node: 1 for node in bfs_tree.nodes()}

# NÓS QUE O BFS NÃO ALCANÇOU
nos_nao_alcancados = set(G.nodes()) - set(bfs_tree.nodes())
print(f"Nós alcançados pelo BFS: {len(bfs_tree.nodes())}")
print(f"Nós não alcançados: {len(nos_nao_alcancados)}")
if nos_nao_alcancados:
  print(f"  {nos_nao_alcancados}")

# PLOTAR
wntr.graphics.plot_network(
  wn,
  node_attribute=node_cluster,
  node_size=10,
  title=f"BFS a partir de {reservatorio}"
)

import matplotlib.pyplot as plt
plt.show()

# TENTATIVA 2: GRAFO NÃO DIRIGIDO → BFS IGNORA O SENTIDO DO FLUXO

# CONVERTER PARA GRAFO NÃO DIRIGIDO
G_und = G.to_undirected()

# BFS NO GRAFO NÃO DIRIGIDO
reservatorio = wn.reservoir_name_list[0]
print(f"Reservatório raiz: {reservatorio}")

bfs_tree = nx.bfs_tree(G_und, source=reservatorio)

# VERIFICAR ALCANCE
nos_nao_alcancados = set(G_und.nodes()) - set(bfs_tree.nodes())
print(f"Nós alcançados pelo BFS: {len(bfs_tree.nodes())}")
print(f"Nós não alcançados: {len(nos_nao_alcancados)}")

# MAPEAR NÓ → CLUSTER
node_cluster = {node: 1 for node in bfs_tree.nodes()}

# PLOTAR
wntr.graphics.plot_network(
  wn,
  node_attribute=node_cluster,
  node_size=10,
  title=f"BFS a partir de {reservatorio}"
)

import matplotlib.pyplot as plt
plt.show()