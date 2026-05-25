# # Este script aloca os nós do modelo hidráulico do SAAE de Mogi Mirim aos polígonos DMC da região, usando as coordenadas dos nós e a geometria dos polígonos DMC.
# # O resultado é um dicionário que associa cada nó a um DMC, e uma lista de nós que não foram alocados a nenhum DMC, mas que provavelmente estão próximos dos DMCs do setor Paulista.
# # O script também imprime um resumo dos resultados, incluindo o número de nós alocados, o número de nós sem DMC e os DMCs encontrados.

import wntr
import geopandas as gpd
from shapely.geometry import Point

# CARREGAR DADOS
inp_file = './dados/base_isolada_v2.inp'
gpkg_file = './dados/Base_SAAE_Mogi_Mirim_v2.gpkg'

wn = wntr.network.WaterNetworkModel(inp_file)
dmc_shp = gpd.read_file(gpkg_file, layer='paulista_dmc')

print(f"CRS do shapefile: {dmc_shp.crs}")
print(f"Coluna DMC — valores únicos: {dmc_shp['DMC'].unique()}")

# GARANTIR CRS COMPATÍVEL
# OBS: As coordenadas do .inp precisam estar no mesmo CRS do shapefile

# ALOCAR NÓS AOS DMCs
node_cluster = {}
sem_dmc = []

for node_name, node in wn.junctions():
  x, y = node.coordinates
  ponto = Point(x, y)
  
  dmc_encontrado = None
  for _, row in dmc_shp.iterrows():
    # usa buffer pequeno para capturar nós na borda
    if row.geometry.buffer(1).contains(ponto):
      dmc_encontrado = row['DMC']
      break
  
  if dmc_encontrado:
    node_cluster[node_name] = dmc_encontrado
  else:
    sem_dmc.append(node_name)

# RESUMO
print(f"\nNós alocados: {len(node_cluster)}")
print(f"Nós sem DMC: {len(sem_dmc)}")
print(f"DMCs encontrados: {set(node_cluster.values())}")

for dmc in sorted(set(node_cluster.values())):
  nos = [n for n, v in node_cluster.items() if v == dmc]
  print(f"  DMC {dmc}: {len(nos)} nós")

if sem_dmc:
  print(f"\nNós sem DMC ({len(sem_dmc)}):")
  for n in sem_dmc[:20]:  # mostra só os 20 primeiros
    node = wn.get_node(n)
    print(f"  {n}: {node.coordinates}")

# PLOTAR
import wntr as wntr_plot
import matplotlib.pyplot as plt

# converter DMC string para número para plotar
dmcs_unicos = sorted(set(node_cluster.values()))
dmc_para_num = {d: i+1 for i, d in enumerate(dmcs_unicos)}
node_cluster_num = {n: dmc_para_num[v] for n, v in node_cluster.items()}

# PLOTAR
wntr_plot.graphics.plot_network(
  wn,
  node_attribute=node_cluster_num,
  node_size=15,
  title="DMCs existentes SAAE — alocação por polígono"
)

plt.show()