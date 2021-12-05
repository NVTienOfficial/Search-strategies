from typing import List
import Node

class Solution:
    '''
    This class represents result is return by each search algorithm
    Include:    + Time to escape
                + The list of expanded nodes
                + The lists of nodes on the path found
    '''

    def __init__(self, expand:List[int] = [], path:List[int] = []) -> None:
        self.expand = expand
        self.path = path
        self.time = len(self.expand)

    def toString(self) -> str:
        '''Transform solution data into a string'''
        sSolution = "Time: " + str(self.time) + '\n'
        sSolution += "Expand nodes: "
        for node in self.expand:
            sSolution += str(node) + " "
        sSolution += '\nPath: '
        for node in self.path:
            sSolution += str(node) + " "
        sSolution += '\n'

        return sSolution