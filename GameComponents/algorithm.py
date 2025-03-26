from pprint import pprint
from random import randint

def create_labirint(cols, rows):
    verticals = [[1] + [0 for i in range(cols - 1)] + [1] for i in range(rows    )]
    horizonts = [[1] * cols] + [([0] * cols) for i in range(rows - 1)] + [[1] * cols]
    map = [[j for j in range(cols * i, cols * (i + 1))] for i in range(rows)]
    
    for row in range(rows - 1):
        for col in range(cols - 1):
            wall = randint(0, 1)
            if wall or map[row][col] == map[row][col + 1]:
                verticals[row][col + 1] = 1
            else:
                group = map[row][col + 1]
                for i in range(row + 1):
                    for j in range(cols):
                        if (map[i][j] == group):
                            map[i][j] = map[row][col]
        for col in range(cols):
            wall = randint(0, 1)
            if wall:
                k = 0
                for i in range(cols):
                    if map[row][i] == map[row][col] and horizonts[row + 1][i] == 0:
                        k += 1
                if k > 1:
                    horizonts[row + 1][col] = 1
                else:
                    map[row + 1][col] = map[row][col]
            else:
                map[row + 1][col] = map[row][col]
                
    for col in range(cols - 1):
        wall = randint(0, 1)
        if wall or map[rows - 1][col] == map[rows - 1][col + 1]:
            verticals[rows - 1][col + 1] = 1
        else:
            group = map[rows - 1][col + 1]
            for i in range(rows):
                for j in range(cols):
                    if (map[i][j] == group):
                        map[i][j] = map[rows - 1][col]
    for col in range(cols - 1):
        if map[rows - 1][col] != map[rows - 1][col + 1]:
            verticals[rows - 1][col + 1] = 0
        group = map[rows - 1][col + 1]
        for j in range(cols):
            if (map[rows - 1][j] == group):
                map[rows - 1][j] = map[rows - 1][col]
    
    
    #pprint(verticals)
    #pprint(horizonts)
    #pprint(map)
    
    start  = (randint(0, cols - 1), randint(0, rows - 1))
    finish = (randint(0, cols - 1), randint(0, rows - 1))
    
    return verticals, horizonts, start, finish
    
if __name__ == '__main__':
    create_labirint(8, 10)