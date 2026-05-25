# Comparar resultado do BFS com DMCs do SAAE
# node_cluster_bfs = resultado do BFS com T6698, T6701, T6702
# node_cluster_saae = resultado da alocação por polígono

import json
import wntr
import geopandas as gpd
from shapely.geometry import Point

# CARREGAR RESULTADO DO BFS
with open('./resultados/node_cluster_bfs.json', 'r') as f:
  node_cluster_bfs = json.load(f)

# CARREGAR RESULTADO DO SAAE (rodar alocação por polígono)
inp_file = './dados/base_isolada_v2.inp'
gpkg_file = './dados/Base_SAAE_Mogi_Mirim_v2.gpkg'

wn = wntr.network.WaterNetworkModel(inp_file)
dmc_shp = gpd.read_file(gpkg_file, layer='paulista_dmc')

node_cluster_saae = {}
for node_name, node in wn.junctions():
  x, y = node.coordinates
  ponto = Point(x, y)
  for _, row in dmc_shp.iterrows():
    if row.geometry.buffer(1).contains(ponto):
      node_cluster_saae[node_name] = row['DMC']
      break

print(f"Nós alocados pelo SAAE: {len(node_cluster_saae)}")
print(f"DMCs SAAE: {set(node_cluster_saae.values())}")

# MAPEAR LABELS DO BFS PARA LABELS DO SAAE
# o BFS usa números (1, 2, 3) e o SAAE usa nomes — precisa descobrir a correspondência
# veja qual label do BFS tem mais nós em comum com qual label do SAAE

dmcs_saae = sorted(set(node_cluster_saae.values()))
clusters_bfs = sorted(set(node_cluster_bfs.values()))

print("Matriz de correspondência (linhas=BFS, colunas=SAAE):")
print(f"{'':>10}", end="")
for d in dmcs_saae:
  print(f"{str(d):>12}", end="")
print()

mapeamento = {}
for c in clusters_bfs:
  nos_bfs = {n for n, v in node_cluster_bfs.items() if v == c}
  print(f"Cluster {c}  ", end="")
  melhor_contagem = 0
  melhor_dmc = None
  for d in dmcs_saae:
    nos_saae = {n for n, v in node_cluster_saae.items() if v == d}
    intersecao = len(nos_bfs & nos_saae)
    print(f"{intersecao:>12}", end="")
    if intersecao > melhor_contagem:
      melhor_contagem = intersecao
      melhor_dmc = d
  mapeamento[c] = melhor_dmc
  print()

print(f"\nMapeamento automático BFS → SAAE: {mapeamento}")

# CALCULAR CONCORDÂNCIA
concordantes = 0
total_comparaveis = 0

for node, cluster_bfs in node_cluster_bfs.items():
  if node in node_cluster_saae:
    total_comparaveis += 1
    dmc_saae = node_cluster_saae[node]
    dmc_bfs_mapeado = mapeamento[cluster_bfs]
    if dmc_bfs_mapeado == dmc_saae:
      concordantes += 1

print(f"\nNós comparáveis: {total_comparaveis}")
print(f"Nós concordantes: {concordantes}")
print(f"Taxa de concordância: {concordantes/total_comparaveis*100:.1f}%")

# SALVAR RESULTADO
import pandas as pd
resultado = {
  'nos_bfs': len(node_cluster_bfs),
  'nos_saae': len(node_cluster_saae),
  'nos_comparaveis': total_comparaveis,
  'nos_concordantes': concordantes,
  'taxa_concordancia': round(concordantes/total_comparaveis*100, 1),
  'mapeamento_bfs_saae': mapeamento
}

with open('./resultados/concordancia.json', 'w') as f:
  json.dump(resultado, f, indent=2)

print("\nResultado salvo em ./resultados/concordancia.json")