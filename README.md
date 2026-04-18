# tfc-grad
 
Repositório do Trabalho Final de Curso em Engenharia Civil — Unicamp (FEC).
 
**Tema:** Redução de Perdas e Eficiência Operacional de Sistemas de Abastecimento de Água — Aplicação de algoritmos de agrupamento para delimitação de Distritos de Medição e Controle (DMCs) no sistema de abastecimento de Mogi Mirim-SP.
 
---
 
## Contexto
 
A delimitação de DMCs é uma etapa fundamental para o controle de perdas em redes de distribuição de água. Este trabalho aplica algoritmos de agrupamento baseados em teoria dos grafos — seguindo o fluxograma de seleção proposto por Pegorini et al. (2024) — ao modelo hidráulico real do município de Mogi Mirim-SP, fornecido pelo SAAE (Serviço Autônomo de Água e Esgotos).
 
O método selecionado pelo fluxograma para as características desta rede é o **BFS (Breadth-First Search)**, aplicado sobre um dígrafo construído a partir do modelo hidráulico.
 
---
 
## Bibliotecas principais
 
### [WNTR](https://wntr.readthedocs.io/) — Water Network Tool for Resilience
Pacote Python desenvolvido pela EPA e Sandia National Laboratories para simulação e análise de redes de distribuição de água. Permite carregar arquivos `.inp` do EPANET, rodar simulações hidráulicas e converter a rede em grafos compatíveis com NetworkX.
 
> **Atenção:** WNTR é compatível apenas com **Python 3.12**. Recomenda-se o uso de ambiente virtual (`.venv`) para isolar a instalação.
 
### [NetworkX](https://networkx.org/)
Biblioteca Python para criação, manipulação e análise de grafos e redes complexas. Usada para aplicar os algoritmos de agrupamento sobre o grafo da rede de distribuição.
 
### [Matplotlib](https://matplotlib.org/)
Usada para visualização dos resultados — plotagem da rede com os clusters identificados.
 
---
 
## Estrutura do repositório
 
```
tfc-grad/
│
├── redundancia.py           # Cálculo do grau médio e análise de redundância da rede
├── clustering_topologico.py # Aplicação exploratória de algoritmos de clusterização (abordagem topológica)
├── clustering_bfs.py        # Aplicação do algoritmo BFS para delimitação dos DMCs (método principal)
├── testes/                  # Scripts intermediários e experimentos
├── resultados/              # Outputs gerados (mapas, tabelas, figuras)
├── dados/                   # Dados do SAAE (não versionado)
├── requirements.txt         # Dependências requisitadas pelo WNTR
├── cronograma.md            # Cronograma de execução do TFC II
└── README.md
```
 
---
 
## Configuração do ambiente
 
```bash
# Criar ambiente virtual com Python 3.12
python3.12 -m venv .venv
 
# Ativar ambiente
.venv\Scripts\activate # (Windows)
source .venv/bin/activate # (MacOS/Linux)

# Atualizar pip
python -m pip install --upgrade pip

# Instalar dependências
pip install wntr networkx matplotlib
# ou
pip install -r requirements.txt
```
 
---
 
## Dados
 
Os arquivos de entrada (modelo hidráulico `.inp` e dados SIG) são fornecidos pelo SAAE de Mogi Mirim-SP e **não estão versionados** neste repositório por questões de confidencialidade.
 
---
 
## Principal referência metodológica
 
Pegorini, M. L. L. et al. (2024). *Critérios para Seleção de Algoritmo de Agrupamento para Divisão de Distritos de Medição e Controle*. XXXI Congreso Latinoamericano de Hidráulica, Medellín.

---

### Orientador

Prof. Dr. José Gilberto Dalfré Filho

### Coorientadora

Prof. Dr. Daniela Bonazzi Sodek