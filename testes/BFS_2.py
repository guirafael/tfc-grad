import wntr
import networkx as nx
import matplotlib.pyplot as plt

# CARREGAR MODELO
inp_file = "./dados/base_isolada_v2.inp"
wn = wntr.network.WaterNetworkModel(inp_file)

# CONVERTER PARA GRAFO NÃO DIRECIONADO
G_und = wn.to_graph().to_undirected()

# RAÍZES: reservatório + tanques
raizes = wn.reservoir_name_list + wn.tank_name_list
print(f"Raízes: {raizes}")

# Dicionário para mapear o nome da raiz para o seu ID numérico (1, 2, 3...)
raiz_para_id = {raiz: i + 1 for i, raiz in enumerate(raizes) if raiz in G_und}

# nx.multi_source_shortest_path encontra o caminho mais curto de QUALQUER uma das fontes
# para todos os nós da rede de forma simultânea.
caminhos_multi_fonte = nx.multi_source_dijkstra_path(G_und, sources=list(raiz_para_id.keys()))

node_cluster = {}
for no, caminho in caminhos_multi_fonte.items():
  raiz_origem = caminho[0] # A raiz que alcançou este nó primeiro é o primeiro elemento do caminho
  node_cluster[no] = raiz_para_id[raiz_origem] # Associa o ID do cluster

print(f"Nós alocados: {len(node_cluster)}")
print(f"Clusters gerados: {set(node_cluster.values())}")
for c in sorted(set(node_cluster.values())):
  nos = [n for n, v in node_cluster.items() if v == c]
  # Encontra o nome da raiz correspondente a esse ID para o print ficar claro
  nome_raiz = [nome for nome, id_c in raiz_para_id.items() if id_c == c][0]
  print(f"  Cluster {c} (Raiz {nome_raiz}): {len(nos)} nós")

# PLOTAGEM
wntr.graphics.plot_network(
  wn,
  node_attribute=node_cluster, # Pinta os nós com as cores dos DMCs
  node_size=30, # Aumenta um pouco o nó para você enxergar os clusters
  title="DMCs propostos — BFS multi-fonte"
)

plt.show()