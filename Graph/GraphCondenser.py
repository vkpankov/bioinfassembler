from .DebrujinGraph import Edge, DebrujinGraph

class GraphCondenser():

    def __init__(self, graph: DebrujinGraph):

        self.graph = graph
        f = DebrujinGraph()

    def FindMaxNonBranchingPaths(self):

        paths = []
        for vertex in self.graph.vertices.values():
            if(not vertex.IsMInNOutVertex(1, 1) and len(vertex.outcoming_edges) > 0):
                for edge in vertex.outcoming_edges:
                    path = [edge]
                    while(path[-1].destination.IsMInNOutVertex(1, 1)):
                        path.append(path[-1].destination.outcoming_edges[0])
                    if(len(path)>1):
                        paths.append(path)
        return paths
    
    def Condense(self):

        paths = self.FindMaxNonBranchingPaths()
        for path in paths:

            path[0].source.outcoming_edges.remove(path[0])
            path[-1].destination.incoming_edges.remove(path[-1])

            coverage_sum = 0
            kmer_count_sum = 0
            new_edge_str: str = path[0].kmer[:self.graph.k - 1]
            for edge in path:
                new_edge_str += edge.kmer[self.graph.k - 1:]
                if(edge != path[-1]):
                    self.graph.RemoveVertex(edge.destination)
                if(edge != path[0]):
                    self.graph.RemoveVertex(edge.source)
                coverage_sum+=edge.coverage
                kmer_count_sum+=edge.kmer_count
                self.graph.RemoveEdge(edge)

            self.graph.edges[new_edge_str] = Edge(path[0].source, path[-1].destination, new_edge_str)
            self.graph.edges[new_edge_str].coverage = coverage_sum
            self.graph.edges[new_edge_str].kmer_count = kmer_count_sum

            path[0].source.outcoming_edges.append(self.graph.edges[new_edge_str])
            path[-1].destination.incoming_edges.append(self.graph.edges[new_edge_str])