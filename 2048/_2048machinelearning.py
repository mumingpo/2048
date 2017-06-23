from _2048board import *
import numpy as np
import tensorflow as tf
from random import randrange as rand

class AI:
    """What should I do? What is machine learning? What is a computer? Help!"""
    ##current logic:
    ##  chain grids on the board into an 'M' like thingy → 'PYTHON'
    ##  with the argmax of the board, create a decreasing chain of nums [128→64→32→16→8→4→2] from the end of PYTHON
    ##  score difference of currentboard from PYTHON_MATRIX by multiplying absolute difference with PYTHON location
    ##  build convolutional neural network minimizing difference
    ##  once a state of minimum score difference has been achieved, escalate the PYTHON to the next power level
    ##  find out that this again doesn't work, delete all code, rinse and repeat

    PYTHON = [(3,0), (2,0), (1,0), (0,0), (0,1), (1,1), (2,1), (3,1), (3,2), (2,2), (1,2), (0,2), (0,3), (1,3), (2,3), (3,3)]
    PYTHON_WEIGHT = np.array([2**i - 1 for i in range(16)])
    @classmethod
    def PYTHON_MATRIX_GENERATOR(cls, maxpower):
        matrix = np.zeros([4, 4], dtype = np.int32)
        index = 15
        while maxpower > 0 and index >= 0:
            matrix[cls.PYTHON[index]] = 2**maxpower - 1
            maxpower -= 1
        return matrix

    def __init__(self, game:Game = None, learning = False):
        if game is None:
            self.game = Game()
        else:
            self.game = game
        self.learning = learning
    

