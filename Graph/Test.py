# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
from Graph import GraphBuilder


# %%
get_ipython().run_line_magic('load_ext', 'gvmagic')


# %%
from Graph import GraphBuilder
gBuilder = GraphBuilder.GraphBuilder()
gBuilder.Build(sequences = ["ACCGT","CGGTA","GATTC"], k = 3)


# %%
def GraphToDot(graph):
    dot_str = 'digraph "Test" { \n'
    for vertex in graph.vertices.values():
        dot_str += f'  {vertex.kmer} [label="{vertex.kmer}"] ;\n'
    for edge in graph.edges.values():
        dot_str += f'{edge.source.kmer} -> {edge.destination.kmer} ;\n'
    dot_str+= "} \n"
    return dot_str


# %%
get_ipython().run_line_magic('dotstr', 'GraphToDot(gBuilder)')


# %%


