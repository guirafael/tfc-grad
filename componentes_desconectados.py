# Este script tem o objetivo de identificar componentes desconectados em um modelo hidráulico isolado da Paulista.wntr
# O script carrega o modelo, converte-o em um grafo, identifica componentes desconectados e verifica se os reservatórios estão na mesma componente.
# Também visualiza as tubulações conectadas aos nós da componente desconectada e as tubulações que fazem a ligação entre a componente desconectada e a componente principal.
# Isso é importante para entender o motivo da desconexão e planejar ações de correção no modelo hidráulico antes de aplicar o algoritmo de estudo.

import wntr
import networkx as nx

# CARREGAR MODELO ISOLADO
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
inp_file = os.path.join(BASE_DIR, 'dados', 'base_isolada_v2.inp')

wn = wntr.network.WaterNetworkModel(inp_file)

# CONVERTER EM GRAFO
G = wn.to_graph()

# IDENTIFICAR COMPONENTES DESCONECTADAS
componentes = list(nx.weakly_connected_components(G))
print(f"Número de componentes: {len(componentes)}")

for i, comp in enumerate(componentes):
  print(f"\nComponente {i+1}: {len(comp)} nós")
  # mostra os nós se for pequena
  if len(comp) < 20:
    print(f"  Nós: {comp}")
  else:
    print(f"  (componente grande)")

# VERIFICAR SE OS RESERVATÓRIOS ESTÃO NA MESMA COMPONENTE
for i, comp in enumerate(componentes):
  reservatorios_na_comp = [r for r in wn.reservoir_name_list if r in comp]
  if reservatorios_na_comp:
    print(f"\nReservatórios na componente {i+1}: {reservatorios_na_comp}")

# VISUALIZAR A COMPONENTE DESCONECTADA
nos_comp2 = {'6000', '2759', '4366', '1393', '4365', 'R6719', '1392'}

print("Tubulações conectadas a esses nós:")
for pipe_name, pipe in wn.pipes():
  if pipe.start_node_name in nos_comp2 or pipe.end_node_name in nos_comp2:
    print(f"  {pipe_name}: {pipe.start_node_name} → {pipe.end_node_name}")

print("\nTubulações que saem da componente 2 e chegam na componente 1:")
comp1 = set(componentes[0])
for pipe_name, pipe in wn.pipes():
  start_in_2 = pipe.start_node_name in nos_comp2
  end_in_2 = pipe.end_node_name in nos_comp2
  start_in_1 = pipe.start_node_name in comp1
  end_in_1 = pipe.end_node_name in comp1
  if (start_in_2 and end_in_1) or (start_in_1 and end_in_2):
    print(f"  {pipe_name}: {pipe.start_node_name} → {pipe.end_node_name}  ← TUBULAÇÃO DE LIGAÇÃO")