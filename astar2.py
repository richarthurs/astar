from math import sqrt
import matplotlib.pyplot as plt
import heapq

# adapted from: https://www.laurentluce.com/posts/solving-mazes-using-python-simple-recursivity-and-a-search/

class Node(object):
    def __init__(self, x, y, obstacle):
        self.obstacle = obstacle;
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0 # node-start
        self.h = 0 # node-target
        self.f = 0 # g + h

class AStar(object):
    def __init__(self):
        print 'hello'
        self.open = []
        heapq.heapify(self.open)
        self.closed = set()
        self.nodes = []
        self.grid_height = 6;
        self.grid_width = 6;

    def init_grid(self, start, end, obstacles):
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) in obstacles:
                    obstacle = False
                else:
                    obstacle = True
                self.nodes.append(Node(x, y, obstacle))

        self.start = self.get_node(*start)
        self.end = self.get_node(*end)

    def heuristic(self, current, target):
        return sqrt((current.x-target.x)**2 + (current.y-target.y)**2)

    def heuristic2(self, cell):
        return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))


    def get_node(self, x, y):
        return self.nodes[x * self.grid_height + y] # they're linear indexed

    def get_neighbours(self, node):
        # CW from right
        neighbours = []
        if node.x < self.grid_width - 1:
            neighbours.append(self.get_node(node.x + 1, node.y))
        if node.y > 0:
            neighbours.append(self.get_node(node.x, node.y - 1))
        if node.x > 0:
            neighbours.append(self.get_node(node.x - 1, node.y))
        if node. y < self.grid_height - 1:
            neighbours.append(self.get_node(node.x, node.y + 1))
        return neighbours

    def show_path(self):
        node = self.end
        path = []
        path.append((node.x, node.y))
        while node.parent is not self.start:
            node = node.parent
            path.append((node.x, node.y))
            print node.x, node.y

        path.append((self.start.x, self.start.y))
        path.reverse()
        return path

    def update_node(self, nextNode, node):
        # updates the next node
        nextNode.g = node.g + 10#node.g + 10 #self.heuristic(nextNode, self.start)
        nextNode.h = self.heuristic2(nextNode) #self.heuristic2(nextNode) #self.heuristic(nextNode, self.end)
        nextNode.f = nextNode.g + nextNode.h
        nextNode.parent = node

    def process(self):
        heapq.heappush(self.open, (self.start.f, self.start)) # add starting node to top of heap
        while len(self.open):
            f, node = heapq.heappop(self.open) # pop node from queue
            self.closed.add(node) # add to closed

            if node is self.end:
                return self.show_path()

            neighbours = self.get_neighbours(node) # grab the neighbours
            for neighbour in neighbours:
                if neighbour.obstacle and neighbour not in self.closed:
                    if (neighbour.f, neighbour) in self.open:
                    # if neighbour is in open list, check if current path is better than the one previously found for this neighbour
                        if neighbour.g > node.g + 10: # previously: > node.g + 10
                            self.update_node(neighbour, node)
                    else:
                        self.update_node(neighbour, node)
                        heapq.heappush(self.open, (neighbour.f, neighbour))


if __name__ == '__main__':
    print 'suh'
    # x = [1,2,3,4]
    # y = [23,21,5,6]
    # plt.plot(x,y)
    # plt.axis([0, 20, 0, 30])
    # plt.show()
    obstacles = ((0, 5), (1, 0), (1, 1), (1, 5), (2, 3),
     (3, 1), (3, 2), (3, 5), (4, 1), (4, 4), (5, 1))


    astar = AStar()
    astar.init_grid([0,0],[5,5], obstacles)
    result = astar.process()

    x, y = zip(*result)
    xobs, yobs = zip(*obstacles)

    plt.axis([-1, 10, -1, 10])
    plt.plot(x,y, 'gd')
    plt.plot(xobs, yobs, 'kx')


    plt.show()



