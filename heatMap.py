"""
 @author     : Bangqi Wang (bwang.will@gmail.com)
 @file       : heatMap.py
 @brief      : Generate heat map for mobility modeling
"""

""" 
Library
"""
import numpy as np
import random as rd


"""
Class
"""
class mall(object):
    """docstring for mall"""
    def __init__(self, row, col, length):
        super(mall, self).__init__()
        self.row = row
        self.col = col
        self.length = length
        self.setPath()
        self.generate_items()
        self.find()
        

    def generate_layout(self):
        """generate layout map:

        0 - 0 - 0 - 0 - 0 - 0 - 0
        |                       |
        0 - 1 - 2 - 3 - 4 - 5 - 0
        |                       |
        0 - 0 - 0 - 0 - 0 - 0 - 0
        |                       |
        0 - 6 - 7 - 8 - 9 - 10- 0
        |                       |
        0 - 0 - 0 - 0 - 0 - 0 - 0
        |
        E

        """
        layout = []
        for i in range(self.height):
            if i % 2:
                temp = [0]
                for item in self.items[i/2]:
                    temp.append(item)
                temp.append(0)
                layout.append(temp)
            else:
                layout.append(np.zeros(self.col+2))            
        self.layout = np.array(layout)


    def generate_items(self):
        """generate graph:

        1 - 2 - 3 - 4 - 5
        |               |
        6 - 7 - 8 - 9 - 10
        |
        E

        """
        self.items = np.arange(self.row*self.col + 1)[1:].reshape(self.row, self.col)
        self.weights = np.zeros(self.row*self.col).reshape(self.row, self.col)


    def setPath(self):
        """set path"""
        self.num = self.row * self.col
        self.width = self.col + 2
        self.height = 2 * self.row + 1
        rd.seed(1)
        self.patten = sorted(rd.sample(np.arange(self.num + 1)[1:], self.length))
        print self.patten


    def find(self):
        """find shortest path"""
        i = 0
        strategy = []
        left, right = -1, -1
        for item in self.patten:
            if item/self.col == left/self.col:
                right = item
            else:
                if left != -1:
                    left_path = left%self.col + item%self.col
                    right_path = 2*self.col + 2 - right%self.col - item%self.col
                    if left_path < right_path:
                        self.set_weight_left(left, item)
                    elif left_path > right_path:
                        self.set_weight_right(right, item)
                    else:
                        self.set_weight_both(left, item)
                left = item
                right = item
        self.set_weight_start(self.patten[0])
        self.set_weight_end(self.patten[-1])


    def set_weight_left(self, start, end):
        """set left path from start to end

        e.g. from 2 to 7:

        1---(2)   3   4   5
        |                
        6---(7)   8   9   10
        
        E
        
        """
        print 'Set left path from {} to {}'.format(start, end)
        row_start = (start-1)/self.col + 1
        row_end = (end-1)/self.col + 1
        col_start = (start-1)%self.col + 1
        col_end = (end-1)%self.col + 1

        for row in range(row_start, row_end+1):
            if row == row_start:
                for col in range(col_start):
                    self.weights[row][col] += 1
            elif row == row_end:
                for col in range(col_end):
                    self.weights[row][col] += 1
            else:
                self.weights[row][0] += 1
        print self.weights
        

    def set_weight_right(self, start, end):
        """set right path from start to end
        
        e.g. from 4 to 9:

        1   2   3   (4)---5
                          |
        6   7   8   (9)---10
        
        E

        """
        print 'Set right path from {} to {}'.format(start, end)
        row_start = (start-1)/self.col + 1
        row_end = (end-1)/self.col + 1
        col_start = (start-1)%self.col + 1
        col_end = (end-1)%self.col + 1
        for row in range(row_start, row_end+1):
            if row == row_start:
                for col in range(col_start-1, self.col):
                    self.weights[row][col] += 1
            elif row == row_end:
                for col in range(col_end, self.col):
                    self.weights[row][col] += 1
            else:
                self.weights[row][self.col-1] += 1
        print self.weights


    def set_weight_both(self, start, end):
        """set both path from start to end

        e.g. from 3 to 8:

        1~~~2~~~(3)---4---5
        \                 |
        6~~~7~~~(8)---9---10
        
        E

        """
        print 'Set both path from {} to {}'.format(start, end)
        row_start = (start-1)/self.col + 1
        row_end = (end-1)/self.col + 1
        col_start = (start-1)%self.col + 1
        col_end = (end-1)%self.col + 1
        for row in range(row_start, row_end+1):
            if row == row_start:
                for col in range(self.col):
                    self.weights[row][col] += 0.5
            elif row == row_end:
                for col in range(self.col):
                    self.weights[row][col] += 0.5
            else:
                self.weights[row][0] += 0.5
                self.weights[row][self.col-1] += 0.5
        self.weights[row_start][col_start-1] += 0.5
        self.weights[row_end][col_end-1] -= 0.5
        print self.weights


    def set_weight_start(self, start):
        """set right path from start to end
        
        e.g. from E to 4:

        1---2---3---(4)   5
        |                 
        6   7   8    9    10
        |
        E

        """
        row_start = (start-1)/self.col + 1
        col_start = (start-1)%self.col + 1
        for row in range(row_start, self.row):
            if row == row_start:
                for col in range(col_start-1):
                    self.weights[row][col] += 1
            else:
                self.weights[row][0] += 1
        print self.weights


    def set_weight_end(self, end):
        """set right path from start to end
        
        e.g. from 9 to E:

        1   2   3   (4)   5

        6---7---8---(9)   10
        |
        E

        """
        row_end = (end-1)/self.col + 1
        col_end = (end-1)%self.col + 1
        for row in range(row_end, self.row):
            if row == row_end:
                for col in range(col_end):
                    self.weights[row][col] += 1
            else:
                self.weights[row][0] += 1
        print self.weights
            

"""
Main function
"""
if __name__ == '__main__':
    row, col, length = 5, 5, 3
    model = mall(row, col, length)
    print model.items
    print model.weights












