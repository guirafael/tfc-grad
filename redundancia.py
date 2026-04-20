import networkx as nx
import wntr

# Determinação do Grau de Redundância da rede
# Grau de Redundância Alto -> Acima de 2.5. Abaixo disso -> Baixo

# CARREGAR MODELO
inp_file = './dados/base_completa_v6.inp'
wn = wntr.network.WaterNetworkModel(inp_file)

# TRANSFORMAR EM GRAFO
G = wn.to_graph()

# GRAU DE REDUNDÂNCIA
# 1º Método
G_und = G.to_undirected()
avg_degree = sum(dict(G_und.degree()).values()) / G_und.number_of_nodes()
print(f"Grau médio: {avg_degree:.2f}")
print(f"Rede com {len(wn.reservoir_name_list)} fontes: {list(wn.reservoir_name_list)}")

# 2º Método
# print("Iniciando cálculo...")
# print(nx.average_node_connectivity(G.to_undirected()))