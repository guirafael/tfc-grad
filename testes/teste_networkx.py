import networkx as nx
from networkx.algorithms.community import girvan_newman
import matplotlib.pyplot as plt

# Criando um grafo de exemplo
G = nx.karate_club_graph()  # Grafo clássico usado em testes de comunidades

# Executando o algoritmo de Girvan-Newman
communities = girvan_newman(G)

# Pegando a primeira divisão em comunidades
first_level_communities = next(communities)
clusters = [list(c) for c in first_level_communities]

print("Comunidades encontradas:")
for i, cluster in enumerate(clusters, start=1):
  print(f"Comunidade {i}: {cluster}")


# Criando dicionário nó -> comunidade
color_map = {}
for i, cluster in enumerate(clusters):
  for node in cluster:
    color_map[node] = i

# Definindo as cores para os nós
node_colors = [color_map[node] for node in G.nodes()]

# Desenhando o grafo
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, node_color=node_colors, with_labels=True, cmap=plt.cm.Set3)
plt.show()