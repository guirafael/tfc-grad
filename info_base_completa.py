# Este script tem o objetivo de realizar uma delimitação preliminar de setores de controle (DMCs) em uma rede de abastecimento de água utilizando algoritmos de agrupamento (community detection) aplicados à estrutura topológica da rede.
# A ideia é identificar grupos de nós que estão mais fortemente conectados entre si do que com o restante da rede, o que pode indicar potenciais DMCs.
# O usuário pode escolher entre diferentes algoritmos de detecção de comunidades, como Greedy Modularity, Girvan-Newman e Label Propagation.
# O resultado é visualizado por meio de um gráfico da rede, onde os nós são coloridos de acordo com o cluster ao qual pertencem.
# Ou seja, é uma delimitação preliminar realizada por meio de algoritmos de agrupamento aplicados à estrutura topológica da rede

import wntr
import matplotlib.pyplot as mp

from networkx.algorithms import community

# CARREGAR MODELO
inp_file = './dados/base_completa_v6.inp'
wn = wntr.network.WaterNetworkModel(inp_file)

# TRANSFORMAR EM GRAFO
G = wn.to_graph()

# ESCOLHER ALGORITMO
print("Escolha o algoritmo:")
print("1 - Greedy Modularity")
print("2 - Girvan-Newman")
print("3 - Label Propagation")

#EXECUTAR ALGORITMO
userinput = input("Digite o número: ")
if userinput == "1":
  communities = list(community.greedy_modularity_communities(G))
elif userinput == "2":
  print("Rodando algoritmo...")
  comp = community.girvan_newman(G)
  communities = list(next(comp))  # primeira divisão
elif userinput == "3":
  G = wn.get_graph().to_undirected()
  communities = list(community.label_propagation_communities(G))
else:
  print("Opção inválida")
  exit()

# CRIAR DICIONÁRIO NÓ → CLUSTER
node_cluster = {}
for i, comm in enumerate(communities):
  for node in comm:
    node_cluster[node] = i

# PLOTAR A REDE
wntr.graphics.plot_network(
  wn,
  node_attribute=node_cluster,
  node_size=20,
  title="Candidatos a DMCs"
)

mp.show()