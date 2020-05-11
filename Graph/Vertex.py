from . import Edge
from typing import List

class Vertex():
    """
        Класс, представляющий вершину графа де-брюина
    """

    def __init__(self, kmer: str, is_reverse: bool = False) -> None:
        self.incoming_edges: List[Edge] = []
        self.outcoming_edges: List[Edge] = []
        self.kmer: str = kmer
        self.rev_complement: Vertex = None
        self.is_reverse: bool = is_reverse

    def IsMInNOutVertex(self, M: int, N: int) -> bool:
        in_len: int = len(self.incoming_edges)
        out_len: int = len(self.outcoming_edges)
        return in_len == M and out_len == N