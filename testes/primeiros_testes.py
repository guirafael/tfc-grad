import scipy as sc
import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as mp
import setuptools as st
import wntr

# CARREGAR MODELO
# Pegar o diretório absoluto do próprio script, independente de onde é executado
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Montar o caminho até o .inp navegando um nível acima (neste caso) e entrando na pasta dados/
inp_file = os.path.join(BASE_DIR, '..', 'dados', 'base_completa_v6.inp')

wn = wntr.network.WaterNetworkModel(inp_file)

# EXPLORAR A REDE
# Obter números de elementos
print("Nós:", len(wn.node_name_list))
print("Tubulações:", len(wn.link_name_list))

# Listar nós e links
print(wn.node_name_list[:10])
print(wn.link_name_list[:10])

# RODAR SIMULAÇÃO HIDRÁULICA
sim = wntr.sim.EpanetSimulator(wn)
results = sim.run_sim()

# ACESSAR RESULTADOS
# Obter pressão nos nós
pressure = results.node['pressure']
print(pressure.head())

# Obter vazão nas tubulações
flow = results.link['flowrate']
print(flow.head())

# TRANSFORMAR EM GRAFO
G = wn.to_graph()
print(type(G))  # Networkx graph
print(nx.number_of_nodes(G))
print(nx.number_of_edges(G))

# PLOTAR A REDE
wntr.graphics.plot_network(wn)
mp.show()