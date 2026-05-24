# Este script aloca os nós do modelo hidráulico do SAAE de Mogi Mirim aos polígonos DMC da região, usando as coordenadas dos nós e a geometria dos polígonos DMC.
# O resultado é um dicionário que associa cada nó a um DMC, e uma lista de nós que não foram alocados a nenhum DMC, mas que provavelmente estão próximos dos DMCs do setor Paulista.
# O script também imprime um resumo dos resultados, incluindo o número de nós alocados, o número de nós sem DMC e os DMCs encontrados.

import wntr
import fiona
import geopandas
from shapely.geometry import Point

# CARREGAR DADOS DO SAAE
inp_file = './dados/base_isolada_v2.inp'
gpkg_file = './dados/Base_SAAE_Mogi_Mirim_v2.gpkg'
wntr = wntr.network.WaterNetworkModel(inp_file)

# VER TODAS AS CAMADAS DO GPKG
camadas = fiona.listlayers(gpkg_file)
print("Camadas disponíveis:")
for c in camadas:
  print(f"  {c}")

dmc_shp = geopandas.read_file(gpkg_file, layer='paulista_dmc')
print(dmc_shp.columns.tolist())  # colunas disponíveis
print(dmc_shp.head())            # primeiros registros
print(f"CRS do shapefile: {dmc_shp.crs}")

# COORDENADAS DOS NÓS VIA WNTR
node_cluster = {}
sem_dmc = []

for node_name, node in wntr.junctions():
  x, y = node.coordinates
  ponto = Point(x, y)
  
# verificar em qual polígono DMC o nó está
  dmc_encontrado = None
  for _, row in dmc_shp.iterrows():
    if row.geometry.contains(ponto):
      dmc_encontrado = row['DMC']
      break
  
  if dmc_encontrado:
    node_cluster[node_name] = dmc_encontrado
  else:
    sem_dmc.append(node_name)

print(f"\nNós alocados: {len(node_cluster)}")
print(f"Nós sem DMC: {len(sem_dmc)}")
print(f"DMCs encontrados: {set(node_cluster.values())}")