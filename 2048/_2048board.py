from random import randrange as rand
from msvcrt import getch as keyin
import os

class Game(object):
    """set up the board and movement for the game 2048"""
    @staticmethod
    def randp(): return rand(10) == 9                                       ##if true return '4' tile else '2'

    def randl(self):                                                        ##return random available location
        return self.availlocs[rand(len(self.availlocs))]

    def addpatl(self):                                                      ##add tile at random availale location
        loc = self.randl()
        self.board[loc[0]][loc[1]] += self.randp() + 1

    @staticmethod
    def merge(lis):                                                         ##merge a list of int in the downward direction, return False if not possible to move
        newlis = [i for i in lis if i]                                      ##cut zeroes
        l = len(newlis)
        if l == 0: return False                                             ##unable to move if no piece is present
        elif l == 1:
            if lis[-1]: return False                                        ##if the only available piece is located toward the end, no move is possible
            else: return [0] * 3 + newlis                                   ##else return [0, 0, 0, num]
        elif l == 2:
            if newlis[0] == newlis[1]: return [0, 0, 0, newlis[0] + 1]      ##if the two nums are equal return [0, 0, 0, num + 1]
            elif lis[-1] and lis[-2]: return False                          ##elif different and located toward end, no move is possible
            else: return [0] * 2 + newlis                                   ##else return [0, 0, num1, num2]
        elif l == 3:
            if newlis[1] == newlis[2]: return [0, 0, newlis[0], newlis[1] + 1]
            elif newlis[0] == newlis[1]: return [0, 0, newlis[0] + 1, newlis[2]]
            elif lis[0] == 0: return False
            else: return [0] + newlis
        else:
            if newlis [2] == newlis[3]:
                if newlis[0] == newlis[1]: return [0, 0, newlis[0] + 1, newlis[2] + 1]
                else: return [0, newlis[0], newlis[1], newlis[2] + 1]
            elif newlis[1] == newlis[2]: return [0, newlis[0], newlis[1] + 1, newlis[3]]
            elif newlis[0] == newlis[1]: return [0, newlis[0] + 1, newlis[2], newlis[3]]
            else: return False

    @staticmethod
    def rotateboard(board, direction):
        if direction == 'up':
            clockwise90 = [list(reversed(col)) for col in zip(*board)]
            return clockwise90
        elif direction == 'down':
            diagonalflip = [list(col) for col in zip(*board)]
            return diagonalflip
        elif direction == 'left':
            verticalflip = [list(reversed(row)) for row in board]
            return verticalflip
        elif direction == 'right':
            harlemshake = [[i for i in row] for row in board]
            return harlemshake
        else: raise Exception("Something shouldn't happen happened and move is not identified.")

    @staticmethod
    def rotateboardback(board, direction):
        if direction == 'up':
            counterclockwise90 = [list(col) for col in reversed(list(zip(*board)))]
            return counterclockwise90
        elif direction == 'down':
            diagonalflip = [list(col) for col in zip(*board)]
            return diagonalflip
        elif direction == 'left':
            verticalflip = [list(reversed(row)) for row in board]
            return verticalflip
        elif direction == 'right':
            harlemshake = [[i for i in row] for row in board]
            return harlemshake
        else: raise Exception("Something shouldn't happen happened and move is not identified.")

    def makemove(self, direction = None, disp = True):
        if direction is None:
            k = ord(keyin())
            while k != 224:                                                 ##for arrow keys, msvcrt.getch() work by returning 224 on first call, and then 72/75/77/80 on second call
                k = ord(keyin())
            k = ord(keyin())
            direction = {72: 'up', 80: 'down', 75: 'left', 77: 'right'}.get(k, 'chicken')
        newboard = self.rotateboard(self.board, direction)                  ##rotate board such that it is always merging right
        moved = False                                                       ##some events only happen when a valid move is made
        newnewboard = []                                                    ##merge rows
        for row in newboard:
            newrow = self.merge(row)
            if newrow:
                newnewboard.append(newrow)
                moved = True
            else: newnewboard.append(row)
        self.board = self.rotateboardback(newnewboard, direction)           ##rotate back
        if moved:
            self.availlocs = list(self.availloc())
            self.addpatl()                                                  ##add a random piece
            self.availlocs = list(self.availloc())
        if disp:
            os.system('cls')
            self.disp()
        return self.checkdeadlock()

    def availloc(self):
        for row in range(4):
            for col in range(4):
                if self.board[row][col] == 0:
                    yield row, col

    def checkdeadlock(self):
        if len(self.availlocs) == 0:                                        ##less expensive check first
            for direction in ['up', 'down', 'left', 'right']:
                newboard = self.rotateboard(self.board, direction)
                for row in newboard:
                    if self.merge(row): return False                        ##if any merge is available, return False
            return True
        else: return False

    def __init__(self, board = None, disp = True):
        if board is None:
            self.board = [[0] * 4 for i in range(4)]
            self.availlocs = list(self.availloc())
            for i in range(2): self.addpatl()
        elif instanceof(board, Game):
            self.board = [[loc for loc in row] for row in board.board]
            self.availlocs = list(self.availloc())
        else:
            self.board = [[loc for loc in row] for row in board]
            self.availlocs = list(self.availloc())
        if disp: self.disp()

    def __str__(self):
        s = ''
        sep = '-' * 41 + '\n'
        blank = ('|' + ' ' * 9) * 4 + '|\n'
        for row in self.board:
            s += sep + blank * 2
            s += '|{:^9}|{:^9}|{:^9}|{:^9}|\n'.format(*[str(2**i) if i else '' for i in row])
            s += blank * 2
        s += '-' * 41
        return s
    def disp(self):
        print(str(self))

    def run(self, disp = True):
        deadlock = self.makemove(disp = disp)
        while deadlock is False:
            deadlock = self.makemove(disp = disp)
        print('You lost.')