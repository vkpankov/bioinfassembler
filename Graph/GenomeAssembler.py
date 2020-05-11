from Graph.DebrujinGraph import DebrujinGraph
from Graph.GraphCondenser import GraphCondenser
from Graph.GraphCleaner import GraphCleaner
from Bio import SeqIO
from typing import List

class GenomeAssembler():

    def _ReadInputFile(self) -> List[str]:
        reads = SeqIO.parse(open(self.inputFileName), "fastq" if "fastq" in self.inputFileName else "fasta")
        sequences: List[str] = []
        for read in reads:
            sequences.append(str(read.seq))
        return sequences

    def _SaveGraph(self, fileName: str):
 
        ind: int = 0
        f=open(fileName, 'w')
        for edge in self.graph.edges.values():
            if(not edge.is_reverse):
                f.write(f">S{ind}, cov:{edge.coverage}, len:{edge.kmer_count}\n")
                f.write(f"{edge.kmer}\n")
                ind+=1
        f.close()

    def __init__(self, inputFileName: str, outputFileName: str, k: int, removeSmallEndingEdges: bool,   removeLowCoveredEdges: bool, minAverageCoverage: float, minEdgeLength: int):

        self.inputFileName: str = inputFileName
        self.outputFileName: str = outputFileName
        self.k = k + 1
        self.removeSmallEndingEdges: bool = removeSmallEndingEdges
        self.removeLowCoveredEdges: bool = removeLowCoveredEdges
        self.minAverageCoverage = minAverageCoverage
        self.minEdgeLength = minEdgeLength
        pass

    def Assemble(self):

        sequences = self._ReadInputFile()
        self.graph = DebrujinGraph()
        self.graph.Build(sequences, self.k)
        condenser = GraphCondenser(self.graph)
        condenser.Condense()
        cleaner = GraphCleaner(self.graph)
        if(self.removeSmallEndingEdges):
            cleaner.RemoveSmallEndingEdges(self.minAverageCoverage, self.minEdgeLength)
            condenser.Condense()
        if(self.removeLowCoveredEdges):
            cleaner.RemoveLowCoveredEdges(self.minAverageCoverage, self.minEdgeLength)
            condenser.Condense()
        
        self._SaveGraph(self.outputFileName)
