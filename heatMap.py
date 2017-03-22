import numpy as np
import random as rd


class mall(object):
    """docstring for mall"""
    def __init__(self, row, col, length):
        super(mall, self).__init__()
        self.row = row
        self.col = col
        self.length = length
        self.setPath()
        self.generate()
        


    def generate(self):
        """generate layout map"""
        self.items = np.arange(self.row*self.col + 1)[1:].reshape(self.row, self.col)
        print self.items
        layout = []
        for i in range(self.height):
            if i % 2:
                temp = [0]
                for item in self.items[i/2]:
                    temp.append(item)
                temp.append(0)
                layout.append(temp)
            # else:
            #     layout.append(np.zeros(self.col+2))            
        self.layout = np.array(layout)


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
        # [part, left_point, right_point]
        # part = 'mid', 'left', 'right'
        part = [0,0,0]
        for location in self.patten:
            while location not in self.items[i]:
                part.append('no')
                i += 1
            





if __name__ == '__main__':
    row, col, length = 4, 4, 3
    model = mall(row, col, length)
    print model.layout












