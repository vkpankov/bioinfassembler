from Graph.Vertex import Vertex
from Graph.Edge import Edge
from typing import List, Dict, DefaultDict

class DebrujinGraph():


    def Build(self, sequences: List[str], k: int):
        self.vertices: Dict[str, Vertex] = {}
        self.edges: Dict[str, Edge] = {}
        self.k: int = k
        for sequence in sequences:
            for i in range(len(sequence) + 1 - k):
                kmer: str = sequence[i:i + k]
                self._AddKmer(kmer)

    def _RevComp(self, kmer: str) -> str:
        tab = str.maketrans("ACGT","TGCA")
        return kmer.translate(tab)[::-1]

    def _AddKmer(self, kmer: str):

        revcomp_kmer: str = self._RevComp(kmer)
        left_kmer: str = kmer[:-1]
        right_kmer: str = kmer[1:]

        revcomp_left_kmer: str = revcomp_kmer[:-1]
        revcomp_right_kmer: str = revcomp_kmer[1:]
        
        if(left_kmer not in self.vertices):
            self.vertices[left_kmer] = Vertex(left_kmer)
        if(revcomp_left_kmer not in self.vertices):
            self.vertices[revcomp_left_kmer] = Vertex(revcomp_left_kmer, is_reverse=True)
        if(right_kmer not in self.vertices):
            self.vertices[right_kmer] = Vertex(right_kmer)
        if(revcomp_right_kmer not in self.vertices):
            self.vertices[revcomp_right_kmer] = Vertex(revcomp_right_kmer, is_reverse=True)

        if(kmer not in self.edges):

            self.edges[kmer] = Edge(source = self.vertices[left_kmer], destination = self.vertices[right_kmer], kmer = kmer)
            self.edges[revcomp_kmer] = Edge(source = self.vertices[revcomp_left_kmer], destination = self.vertices[revcomp_right_kmer], kmer = revcomp_kmer)

            self.vertices[left_kmer].outcoming_edges.append(self.edges[kmer])
            self.vertices[right_kmer].incoming_edges.append(self.edges[kmer])

            self.vertices[revcomp_left_kmer].outcoming_edges.append(self.edges[revcomp_kmer])
            self.vertices[revcomp_right_kmer].incoming_edges.append(self.edges[revcomp_kmer])
        else:
            self.edges[kmer].coverage+=1
            self.edges[revcomp_kmer].coverage+=1

    def RemoveVertex(self, vertex: Vertex) -> None:
        self.vertices.pop(vertex.kmer, None)
        self.vertices.pop(self._RevComp(vertex.kmer), None)

    def RemoveEdge(self, edge: Edge) -> None:
        self.edges.pop(edge.kmer, None)
        self.edges.pop(self._RevComp(edge.kmer),  None)

    def RemoveSmallEndingEdges(self, min_coverage: float, min_length: int):
        while(True):
            removing_vertices = []
            for vertex in self.vertices.values():
                if(vertex.IsMInNOutVertex(1, 0)):
                    edge = vertex.incoming_edges[0]
                    if(edge.coverage / edge.kmer_count < min_coverage or edge.kmer_count < min_length):
                        edge.source.outcoming_edges.remove(edge)
                        self.edges.pop(edge.kmer, None)
                        removing_vertices.append(vertex)

                elif(vertex.IsMInNOutVertex(0, 1)):
                    edge = vertex.outcoming_edges[0]
                    if(edge.coverage / edge.kmer_count < min_coverage or edge.kmer_count < min_length):
                        edge.destination.incoming_edges.remove(edge)
                        self.edges.pop(edge.kmer, None)
                        removing_vertices.append(vertex)
            if(len(removing_vertices) == 0):
                break
            for vertex in removing_vertices:
                self.RemoveVertex(vertex)

    def RemoveLowCoveredEdges(self, min_coverage: float, min_length: int):

        removing_edges = []

        for edge in self.edges.values():
            if(edge.coverage/edge.kmer_count < min_coverage or edge.kmer_count < min_length):
                edge.source.outcoming_edges.remove(edge)
                edge.destination.incoming_edges.remove(edge)
                removing_edges.append(edge)
        for edge in removing_edges:
            self.edges.pop(edge.kmer, None) 