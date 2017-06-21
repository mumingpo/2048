from _2048board import *
import tensorflow as tf

class ai:
    """What should I do? What is machine learning? What is a computer? Help!"""
    def __init__(self, game:Game = None):
        if game is None:
            self.game = Game()
        else:
            self.game = game


