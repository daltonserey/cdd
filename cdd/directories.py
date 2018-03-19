import os

class Directories:

    def __init__(self, directories):
        self.data = directories


    def __contains__(self, d):
        dirs = self.data
        index = next((i for i in xrange(len(dirs)) if dirs[i][0] == d), len(dirs))
        return index < len(dirs)
        

    def add(self, d):
        dirs = self.data
        index = next((i for i in xrange(len(dirs)) if dirs[i][0] == d), len(dirs))
        if index == len(dirs):
            dirs.append([d, 0])

    def remove(self, d):
        dirs = self.data
        index = next((i for i in xrange(len(dirs)) if dirs[i][0] == d), len(dirs))
        if index < len(dirs):
            dirs.pop(index)

    def hit(self, d):
        dirs = self.data
        index = next((i for i in xrange(len(dirs)) if dirs[i][0] == d), len(dirs))
        if index < len(dirs):
            dirs[index][1] += 1
            dirs.sort(key=lambda e: e[1], reverse=True)
        


