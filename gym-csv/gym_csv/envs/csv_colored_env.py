# https://github.com/openai/gym/blob/849da90011f877853589c407c170d3c07f680d52/gym/core.py
# https://github.com/openai/gym/blob/849da90011f877853589c407c170d3c07f680d52/gym/envs/toy_text/frozen_lake.py
# https://github.com/openai/gym/blob/849da90011f877853589c407c170d3c07f680d52/gym/envs/toy_text/discrete.py
# https://www.oreilly.com/learning/introduction-to-reinforcement-learning-and-openai-gym
# https://towardsdatascience.com/reinforcement-learning-with-openai-d445c2c687d2

import gym
from gym.envs.toy_text import discrete
import numpy as np
from enum import Enum

# X points down (rows)(v), Y points right (columns)(>), Z would point outwards.
RIGHT = 0  # > Increase Y (column)
UP = 1  # ^ Decrease X (row)
LEFT = 2 # < Decrease Y (column)
DOWN = 3    # v Increase X (row)


class CsvColoredEnv(discrete.DiscreteEnv):
    """
    Has the following members
    - nS: number of states
    - nA: number of actions
    - P: transitions (*)
    - isd: initial state distribution (**)
    (*) dictionary dict of dicts of lists, where
      P[s][a] == [(probability, nextstate, reward, done), ...]
    (**) list or array of length nS
    """
    metadata = {'render.modes': ['human']}

    def __init__(self):
        # Remember: X points down, Y points right, thus Z points outwards.
        # hard-coded vars (begin)
        inFileStr = 'map1.csv'
        initX = 2
        initY = 2
        goalX = 7
        goalY = 7
        # hard-coded vars (end)

        self.map = CharMap(inFileStr, [initX, initY], [goalX, goalY])
        self.nrow = nrow = len(self.map.charMap)
        self.ncol = ncol = len(self.map.charMap[0])

        nS = nrow * ncol # nS: number of states
        nA = 4 # nA: number of actions
        P = {s : {a : [] for a in range(nA)} for s in range(nS)} # transitions (*), filled in at the for loop below.
        isd = np.zeros((nrow, ncol)) # initial state distribution (**)
        isd[initX][initY] = 1
        isd = isd.astype('float64').ravel() # ravel() is like flatten(). However, astype('float64') is just in case.

        def to_s(row, col):
            return row*ncol + col

        def inc(col, row, a): # Assures we will not go off limits.
            if a == LEFT:
                col = max(col-1,0)
            elif a == DOWN:
                row = min(row+1,nrow-1)
            elif a == RIGHT:
                col = min(col+1,ncol-1)
            elif a == UP:
                row = max(row-1,0)
            return (col, row)

        for row in range(nrow): # Fill in P[s][a] transitions and rewards
            for col in range(ncol):
                s = to_s(row, col)
                for a in range(4):
                    li = P[s][a] # In Python this is not a deep copy, therefore we are appending to actual P[s][a] !!

                    tag = int(self.map.charMap[col][row].c)
                    if tag == 4: # goal
                        li.append((1.0, s, 1.0, True)) # (probability, nextstate, reward, done)
                    elif tag == 1: # wall
                        li.append((1.0, s, -500.0, True)) # (probability, nextstate, reward, done) # Some algorithms fail with reward -float('inf')
                    else: # e.g. tag == 0
                        newrow, newcol = inc(row, col, a)
                        newstate = to_s(newrow, newcol)
                        li.append((1.0, newstate, 0.0, False)) # (probability, nextstate, reward, done)

        super(CsvColoredEnv, self).__init__(nS, nA, P, isd)

    # DO NOT UNCOMMENT, LET 'discrete.DiscreteEnv' IMPLEMENT IT!
    #def step(self, action):
    #    print('CsvEnv.step', action)

    # DO NOT UNCOMMENT, LET 'discrete.DiscreteEnv' IMPLEMENT IT!
    #def reset(self):
    #    print('CsvEnv.reset')

    def render(self, mode='human'):
        #print('CsvEnv.render', mode)

        row, col = self.s // self.ncol, self.s % self.ncol # Opposite of ravel().
        self.map.check([col, row])
        self.map.set_current([col, row])

        self.map.dump()

    def close(self):
        print('CsvColoredEnv.close')


class Output(Enum):
    """
    Enumerate to change the standard output format.
    NONE: sys.stdout = os.devnull -> no output is printed
    BASE: cells are printed with their number codes (0 -> empty, 1 -> wall...)
    COLORED: cells are printed with thier color codes (white -> empty, black -> wall...)
    """
    NONE = 'none'
    BASE = 'base'
    COLORED = 'colored'


OUTPUT_MODE = Output.COLORED


class Colors:
    """
    ANSI color codes (source: https://en.wikipedia.org/wiki/ANSI_escape_code).
    """

    ESC = "\033"
    BLINK = "5"
    FG_BLACK = "30"
    FG_RED = "31"
    FG_GREEN = "32"
    FG_YELLOW = "33"
    FG_BLUE = "34"
    FG_MAGENTA = "35"
    FG_CYAN = "36"
    FG_WHITE = "37"
    BG_BLACK = "40"
    BG_RED = "41"
    BG_GREEN = "42"
    BG_YELLOW = "43"
    BG_BLUE = "44"
    BG_MAGENTA = "45"
    BG_CYAN = "46"
    BG_WHITE = "47"


class CharMapCell:
    """
    Wrapper for chars that allows formatting at printing.
    """

    RESET = Colors.ESC + "[0m"
    EMPTY = Colors.ESC + "[" + Colors.FG_WHITE + ";" + Colors.BG_WHITE + "m"
    WALL = Colors.ESC + "[" + Colors.FG_BLACK + ";" + Colors.BG_BLACK + "m"
    NEW = Colors.ESC + "[" + Colors.FG_CYAN + ";" + Colors.BG_CYAN + "m"
    VISITED = Colors.ESC + "[" + Colors.FG_BLUE + ";" + Colors.BG_BLUE + "m"
    C_VISITED = Colors.ESC + "[" + Colors.BLINK + ";" + Colors.BG_BLUE + "m"
    START = Colors.ESC + "[" + Colors.FG_GREEN + ";" + Colors.BG_GREEN + "m"
    C_START = Colors.ESC + "[" + Colors.BLINK + ";" + Colors.BG_GREEN + "m"
    END = Colors.ESC + "[" + Colors.FG_RED + ";" + Colors.BG_RED + "m"
    C_END = Colors.ESC + "[" + Colors.BLINK + ";" + Colors.BG_RED + "m"


    def __init__(self, c):
        self.c = str(c)
        self.is_current = False
        self.is_new = True if self.c == "2" else False

    def __eq__(self, o):
        if isinstance(o, CharMap):
            return self.c == o.c
        elif isinstance(o, int):
            return self.c == str(o)
        elif isinstance(o, str):
            return self.c == o
        else:
            return False

    def __add__(self, o):
        if isinstance(o, CharMap):
            return  str(self) + str(o)
        else:
            raise TypeError("invalid operation between", type(self), "and", type(o))

    def __str__(self):
        if OUTPUT_MODE == Output.BASE:  # just char printing
            return self.c
        elif OUTPUT_MODE == Output.COLORED:  # colored printing
            if self.c == "0":
                return self.EMPTY + self.c + self.RESET
            elif self.c  == "1":
                return self.WALL + self.c + self.RESET
            elif self.c == "2":
                if self.is_new:
                    return self.NEW + self.c + self.RESET
                if self.is_current:
                    return self.C_VISITED + "X" + self.RESET
                return self.VISITED + self.c + self.RESET
            elif self.c == "3":
                if self.is_current:
                    return self.C_START + "X" + self.RESET
                return self.START + self.c + self.RESET
            elif self.c == "4":
                if self.is_current:
                    return self.C_END + "X" + self.RESET
                return self.END + self.c + self.RESET
            else:
                return self.c
        else:
            return ""


class CharMap:
    """
    A map that represents the C-Space.
    """

    def __init__(self, filename, start=None, end=None):
        self.charMap = []
        self.aux = None

        self.read(filename)
        self.start = start
        self.end = end

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, s):
        """
        Start setter. Also adds start position as root in nodes tree.
        Raise exception if s position is non-existent or occupied.

        s: start position ([int, int])
        """
        if s is not None:
            self.charMap[s[0]][s[1]] = CharMapCell(3)
        self.__start = s

    @property
    def end(self):
        return self.__end

    @end.setter
    def end(self, e):
        """
        End setter.
        Raise exception if e position is non-existent or occupied.

        e: end position ([int, int])
        """
        if e is not None:
            self.charMap[e[0]][e[1]] = CharMapCell(4)
        self.__end = e

    def read(self, filename):
        """
        Reads map from file and save it at charMap attribute.
        Raise exception if map file is not found.

        filename: path to file (str).
        """
        try:
            with open(filename) as f:
                line = f.readline()
                while line:
                    charLine = line.strip().split(',')
                    l = []
                    for c in charLine:
                        l.append(CharMapCell(c))
                    self.charMap.append(l)
                    line = f.readline()
        except FileNotFoundError:
            print("[Error] Map not found.", file=sys.stderr)

    def dump(self):
        """
        Prints map.
        """

        for line in self.charMap:
            l = ""
            for char in line:
                l += str(char)
            print(l)
        print()  # empty line behind map

    def check(self, cell):
        """
        Check if cell is end or not visited.

        cell: current cell ([int, int])

        return: 4 if goal_found else -1
        """

        if( self.charMap[cell[0]][cell[1]] == '4' ):  # end
            return 4
        elif ( self.charMap[cell[0]][cell[1]] == '0' ):  # empty
            self.charMap[cell[0]][cell[1]] = CharMapCell(2)
        return -1

    def set_current(self, cell):
        """
        Set cell as current for displaying reasons.
        """

        if self.aux is not None:
            self.charMap[self.aux[0]][self.aux[1]].is_current = False
        self.aux = cell
        self.charMap[cell[0]][cell[1]].is_current = True

    def clear_news(self):
        """
        Set all cells as not news for displaying reasons.
        """

        for row in self.charMap:
            for c in row:
                c.is_new = False

    def reset(self):
        """
        Set all cells as not visited, clear tree nodes and reser checked cells counter.
        """
        self.nodes = []
        self.start = self.start
        self.end = self.end

        for row in self.charMap:
            for c in row:
                if c == "2":
                    c.c = "0"
