import wntr
import networkx as nx

# CARREGAR MODELO ISOLADO
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
inp_file = os.path.join(BASE_DIR, 'dados', 'base_isolada_v2.inp')

wn = wntr.network.WaterNetworkModel(inp_file)

# OBTER INFORMAÇÕES BÁSICAS
print(f"Nós de junção: {len(wn.junction_name_list)}")
print(f"Reservatórios: {wn.reservoir_name_list}")
print(f"Tanques: {len(wn.tank_name_list)}")
print(f"Tubulações: {len(wn.pipe_name_list)}")

# CONVERTER EM GRAFO
G = wn.to_graph()
print(f"\nTipo do grafo: {type(G)}")
print(f"Nós no grafo: {G.number_of_nodes()}")
print(f"Arestas no grafo: {G.number_of_edges()}")

# GRAU MÉDIO DO SETOR ISOLADO
G_und = G.to_undirected()
avg_degree = sum(dict(G_und.degree()).values()) / G_und.number_of_nodes()
print(f"Grau médio do setor: {avg_degree:.2f}")

# VERIFICAR CONECTIVIDADE
print(f"Grafo conectado: {nx.is_weakly_connected(G)}")

# Se o Grafo estiver desconectado, identificar componentes e resolver o problema de conexão em 'componentes_desconectados.py'