import os
import typing
from typing import List
from Problem import Problem
from Solution import Solution
from Algorithm.UCS import Uniform_cost_Search as UCS
from Algorithm.IDS import Iterative_deeping_Search as IDS
from Algorithm.GBFS import Greedy_best_first_Search as GBFS
from Algorithm.Astar import A_star_Search as Astar
from matplotlib import pyplot as plt
import numpy as np

class Program:
    '''
    
    Program class is used for I/O functions
    
    '''

    def __init__(self) -> None:
        self.solutions = {}

    def visual(self):
        '''Visualize problem and solution'''
        visualize(self)

    # I/O functions
    def Input(self, filename:str) -> bool:
        '''Program input from INPUT folder'''
        filename += '.txt'
        if os.path.isfile(os.path.join('../INPUT', filename)):
            self.finput = filename
            filepath = os.path.join('../INPUT', filename)
            N, adj, dest = self.readData(filepath)
            if N!=None and adj != None and dest != None:
                self.problem = Problem(N=N, adjacency=adj, goal=dest)
                return True
        print('Invalid filename')
        return False
            

    def readData(self, filepath) -> typing.Tuple[int, list[list[int]], int]:
        '''Return size(int), adjacency list(list int), and exit(int) of problem from reading input file'''
        if not os.path.exists(filepath):         # if path is not exit return None
            print('Non-exist file')
            return None, None, None

        file = open(filepath, "r")

        N = (int)(file.readline())

        adjacency = []
        for i in range(0, N*N):
            line = file.readline()
            adj = []
            if line not in ['\n', '\r\n']:
                tmp = line.split(' ')
                for x in tmp:
                    adj.append(int(x))
            adjacency.append(adj)

        goal = (int)(file.readline())

        file.close()                             

        return N, adjacency, goal

    def Output(self, filename = "") -> None:
        '''Program output to OUTPUT folder and console'''
        # print to console
        print('\nResult:\n')
        print('File: ', self.finput, '\n')
        for algo, solution in self.solutions.items():
            print(algo)
            print('Time: ', solution.time)
            print('Expand node:', solution.expand)
            print('Path: ', solution.path)
            print('')
        print('\n\n')

        # print to output file
        name = self.finput.replace(".txt", "")            # Output filename's prefix is as input filename
        self.foutput = name + "_out.txt"                     # plus tail _out
        if filename == "":
            filepath = '../OUTPUT/' + self.foutput               # path file in OUTPUT folder
        else:
            filepath = '../OUTPUT/' + filename
        self.writeData(filepath=filepath)
        
    def writeData(self, filepath:str) -> None:
        '''Write a solution(time, expanded node, path) to output file'''
        file = open(filepath, 'w')                          

        for algo, solution in self.solutions.items():
            file.write(algo + '\n')
            file.write(solution.toString())

        file.close()

    # Solve problem
    def solve(self, algorithm:str) -> Solution:
        '''Solve the problem with a search algorithm and return a solution'''
        tmp_problem = self.problem

        algorithm = algorithm.upper()

        if algorithm == 'UCS':
            tmp_problem.solution = UCS(tmp_problem)
        elif algorithm == 'IDS':
            tmp_problem.solution = IDS(tmp_problem)
        elif algorithm == 'GBFS':
            tmp_problem.solution = GBFS(tmp_problem)
        elif algorithm == 'A*':
            tmp_problem.solution = Astar(tmp_problem)

        self.solutions[algorithm] = tmp_problem.solution



def visualize(program: Program):
    '''Visual 4 search strategies in a figure with mathplotlib and numpy'''
    N = program.problem.N

    # maze is a 3D matrix:
    #       First dimension:    row
    #       Second dimension:   col
    #       Third dimension:    Adjacency list (left, right, up, down) with value 1: wall, 0: no wall
    #                       and status with value 0: not expand, 1: expand, 2: path
    maze = np.zeros((N, N, 5), dtype=np.uint8)

    # image is used to plot
    image = np.full((N*10, N*10, 3), [255, 255, 255])

    goal = program.problem.goal
    goal_row = goal % N
    goal_col = goal // N
    start = program.problem.initial
    start_row = start % N
    start_col = start // N

    adj = program.problem.transition_model

    solution = program.solutions

    for node, neighbors in adj.items():
        row = node % N
        col = node // N

        for i in range(0, 4):
            maze[row, col, i] = 1

        for neighbor in neighbors.values():
            if neighbor == 'l':
                maze[row, col, 0] = 0
            if neighbor == 'r':
                maze[row, col, 1] = 0
            if neighbor == 'u':
                maze[row, col, 2] = 0
            if neighbor == 'd':
                maze[row, col, 3] = 0

    for row in range(0, N):
        for col in range(0, N):
            cell = maze[row, col]
            for i in range(10*row,10*row+9):
                image[i, range(10*col, 10*col+9)] = [255, 255, 255]

            if cell[0] == 1:
                image[range(10*row, 10*row+9), 10*col] = [0, 0, 0]
            if cell[1] == 1:
                image[range(10*row, 10*row+9), 10*col+9] = [0, 0, 0]
            if cell[2] ==1:
                image[10*row, range(10*col, 10*col+9)] = [0, 0, 0]
            if cell[3] == 1:
                image[10*row+9, range(10*col, 10*col+9)] = [0, 0, 0]

    for i in range(10*goal_row, 10*goal_row+9):
        image[i, range(10*goal_col, 10*goal_col+9)] = [255, 77, 77]

    for i in range(10*start_row, 10*start_row+9):
        image[i, range(10*start_col, 10*start_col+9)] = [153, 255, 51]

    fig, ax = plt.subplots(nrows=2, ncols=2)
    fig.suptitle(program.finput)

    for r in range(0, 2):
        for c in range(0, 2):
            ax[r][c].axis('off')
            ax[r][c].axis('off')
            img = image.copy()

            if r == 0 and c == 0:
                algo = "UCS"
            elif r == 0 and c == 1:
                algo = "IDS"
            elif r == 1 and c == 0:
                algo = "GBFS"
            else:
                algo = "A*"
            sol = solution[algo]

            ax[r][c].set_title(algo)

            expand = sol.expand
            path = sol.path
            ax[r][c].imshow(img, interpolation='none')
            for node in expand:
                node_row = node % N
                node_col = node // N

                for i in range(10*node_row, 10*node_row+10):
                    for j in range(10*node_col, 10*node_col+10):
                        if not np.array_equal(img[i, j], [0, 0, 0]):
                            img[i, j] = [153, 255, 51]
                
                plt.pause(0.1)
                ax[r][c].imshow(img, interpolation='none')

            for node in path:
                node_row = node % N
                node_col = node // N

                for i in range(10*node_row, 10*node_row+10):
                    for j in range(10*node_col, 10*node_col+10):
                        if not np.array_equal(img[i, j], [0, 0, 0]):
                            img[i, j] = [51, 153, 255]
                
                plt.pause(0.1)
                ax[r][c].imshow(img, interpolation='none')

    plt.show()