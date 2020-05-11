from . import Vertex, Edge
class Edge():
    """
        Класс, представляющий ребро графа де-брюина
    """
    
    def __init__(self, source: Vertex, destination: Vertex, kmer: str, is_reverse: bool = False) -> None:
        self.source: Vertex = source
        self.destination: Vertex = destination
        self.coverage: int = 1
        self.kmer_count: int = 1
        self.kmer: str = kmer
        self.rev_complement: Edge = None
        self.is_reverse: bool = is_reverse