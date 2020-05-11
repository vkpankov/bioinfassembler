from typing import List, Dict, DefaultDict

class Vertex():

    def __init__(self, kmer: str, is_reverse: bool = False) -> None:
        self.incoming_edges: List[Edge] = []
        self.outcoming_edges: List[Edge] = []
        self.kmer: str = kmer
        self.rev_complement: Vertex
        self.is_reverse: bool = is_reverse

    def IsMInNOutVertex(self, M: int, N: int) -> bool:
        in_len: int = len(self.incoming_edges)
        out_len: int = len(self.outcoming_edges)
        return in_len == M and out_len == N

class Edge():
    
    def __init__(self, source: Vertex, destination: Vertex, kmer: str, is_reverse: bool = False) -> None:
        self.source: Vertex = source
        self.destination: Vertex = destination
        self.coverage: int = 1
        self.kmer_count: int = 1
        self.kmer: str = kmer
        self.rev_complement: Edge
        self.is_reverse: bool = is_reverse

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

            self.edges[kmer] = Edge(source = self.vertices[left_kmer], destination = self.vertices[right_kmer], kmer = kmer, is_reverse=False)
            self.edges[revcomp_kmer] = Edge(source = self.vertices[revcomp_left_kmer], destination = self.vertices[revcomp_right_kmer], kmer = revcomp_kmer, is_reverse=True)

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
