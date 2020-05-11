from .DebrujinGraph import Edge, Vertex, DebrujinGraph
from typing import List

class GraphCleaner():

    def __init__(self, graph: DebrujinGraph) -> None:
        self.graph = graph
        
        
    def RemoveSmallEndingEdges(self, min_coverage: float, min_length: int):

        while(True):
            removing_vertices: List[Vertex] = []
            for vertex in self.graph.vertices.values():
                if(vertex.IsMInNOutVertex(1, 0)):
                    edge = vertex.incoming_edges[0]
                    if(edge.coverage / edge.kmer_count < min_coverage or edge.kmer_count < min_length):
                        edge.source.outcoming_edges.remove(edge)
                        self.graph.edges.pop(edge.kmer, None)
                        removing_vertices.append(vertex)

                elif(vertex.IsMInNOutVertex(0, 1)):
                    edge: Edge = vertex.outcoming_edges[0]
                    if(edge.coverage / edge.kmer_count < min_coverage or edge.kmer_count < min_length):
                        edge.destination.incoming_edges.remove(edge)
                        self.graph.edges.pop(edge.kmer, None)
                        removing_vertices.append(vertex)
            if(len(removing_vertices) == 0):
                break
            for vertex in removing_vertices:
                self.graph.RemoveVertex(vertex)

    def RemoveLowCoveredEdges(self, min_coverage: float, min_length: int):

        removing_edges: List[Edge] = []
        for edge in self.graph.edges.values():
            if(edge.coverage/edge.kmer_count < min_coverage or edge.kmer_count < min_length):
                edge.source.outcoming_edges.remove(edge)
                edge.destination.incoming_edges.remove(edge)
                removing_edges.append(edge)
        for edge in removing_edges:
            self.graph.edges.pop(edge.kmer, None) 