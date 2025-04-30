from pprint import pprint
from random import randint
import json

class Labirint:
    doors = 10
    
    def __init__(self, cols, rows):
        self.labirint = {'cols': cols, 'rows': rows,
                        'verticals': [], 'horizonts': [],
                        'start': (0, 0), 'finish': (0, 0),
                        'doors': [], 'buttons': [],
                        'groups': [[0 for i in range(cols)] for i in range(rows)],
                        'spawn_target': []}
        
        self.generate_labirint()
        for i in range(self.doors):
            self.generate_door(i)
        #self.store_level()
        self.store_level('Data/level.json')
        
    def get_labirint(self):
        return self.labirint

    def generate_labirint(self):
        cols, rows = self.labirint['cols'], self.labirint['rows']
        verticals = [[0] * (cols + 1)] + [[1] + [0 for _ in range(cols - 1)] + [1] for _ in range(rows)]
        horizonts = [[0] + [1] * cols] + [([0] * (cols + 1)) for _ in range(rows - 1)] + [[0] + [1] * cols]
        map = [[j for j in range(cols * i, cols * (i + 1))] for i in range(rows)]
        
        for row in range(rows - 1):
            for col in range(cols - 1):
                wall = randint(0, 1)
                if wall or map[row][col] == map[row][col + 1]:
                    verticals[row + 1][col + 1] = 1
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
                        if map[row][i] == map[row][col] and horizonts[row + 1][i + 1] == 0:
                            k += 1
                    if k > 1:
                        horizonts[row + 1][col + 1] = 1
                    else:
                        map[row + 1][col] = map[row][col]
                else:
                    map[row + 1][col] = map[row][col]
                    
        for col in range(cols - 1):
            wall = randint(0, 1)
            if wall or map[rows - 1][col] == map[rows - 1][col + 1]:
                verticals[rows][col + 1] = 1
            else:
                group = map[rows - 1][col + 1]
                for i in range(rows):
                    for j in range(cols):
                        if (map[i][j] == group):
                            map[i][j] = map[rows - 1][col]
        for col in range(cols - 1):
            if map[rows - 1][col] != map[rows - 1][col + 1]:
                verticals[rows][col + 1] = 0
            group = map[rows - 1][col + 1]
            for j in range(cols):
                if (map[rows - 1][j] == group):
                    map[rows - 1][j] = map[rows - 1][col]
                    
        self.labirint['verticals'] = verticals
        self.labirint['horizonts'] = horizonts
        self.labirint['start']  = (randint(0, self.labirint['cols'] - 1), randint(0, self.labirint['rows'] - 1))
        self.labirint['finish'] = (randint(0, self.labirint['cols'] - 1), randint(0, self.labirint['rows'] - 1))
        while (self.labirint['start'][0] == self.labirint['finish'][0] or self.labirint['start'][1] == self.labirint['finish'][1]):
            self.labirint['finish'] = (randint(0, self.labirint['cols'] - 1), randint(0, self.labirint['rows'] - 1))
        self.labirint['spawn_target'].append((self.labirint['start'], self.labirint['finish']))

    def generate_door(self, index):
        door = 'verticals' if randint(0, 1) else 'horizonts'
        
        if door == 'verticals':
            i, j = randint(1, self.labirint['rows']), randint(1, self.labirint['cols'] - 1)
            while self.labirint[door][i][j]:
                i, j = randint(1, self.labirint['rows']), randint(1, self.labirint['cols'] - 1)
        elif door == 'horizonts':
            i, j = randint(1, self.labirint['rows'] - 1), randint(1, self.labirint['cols'])
            while self.labirint[door][i][j]:
                i, j = randint(1, self.labirint['rows'] - 1), randint(1, self.labirint['cols'])
            
        self.generate_button(door, [i, j], index)
        self.labirint['doors'].append((door, [i, j], index))

    def generate_button(self, door, door_pos, index):
        if door == 'verticals':
            p1 = [door_pos[1] - 1, door_pos[0] - 1]
            p2 = [door_pos[1]    , door_pos[0] - 1]
        elif door == 'horizonts':
            p1 = [door_pos[1] - 1, door_pos[0] - 1]
            p2 = [door_pos[1] - 1, door_pos[0]    ]
            
        old_group = self.labirint['groups'][p1[1]][p1[0]]
        for i, grp in enumerate(self.labirint['spawn_target']):
            if self.labirint['groups'][grp[0][1]][grp[0][0]] == old_group:
                start_pos, finish_pos = grp[0], grp[1]
                self.labirint['spawn_target'].pop(i)
                
        self.labirint[door][door_pos[0]][door_pos[1]] = 1
        group_1, group_2 = index * 2 + 1, index * 2 + 2
        self.find_path(p1, old_group, group_1)
        self.find_path(p2, old_group, group_2)
        self.labirint[door][door_pos[0]][door_pos[1]] = 0
        
        start_grp, finish_grp = self.labirint['groups'][start_pos[1]][start_pos[0]], self.labirint['groups'][finish_pos[1]][finish_pos[0]]
        if start_grp == finish_grp:
            grp = group_1 if start_grp == group_2 else group_2
            x, y = (randint(0, self.labirint['cols'] - 1), randint(0, self.labirint['rows'] - 1))
            while self.labirint['groups'][y][x] != grp:
                x, y = (randint(0, self.labirint['cols'] - 1), randint(0, self.labirint['rows'] - 1))
                
            if finish_pos == self.labirint['finish']:
                self.labirint['finish'] = (x, y)
            else:
                for btn in self.labirint['buttons']:
                    if (btn[0], btn[1]) == finish_pos:
                        btn[0], btn[1] = (x, y)
                        
            self.labirint['buttons'].append([finish_pos[0], finish_pos[1], index])
                        
            self.labirint['spawn_target'].append((start_pos, finish_pos))
            p2_grp = self.labirint['groups'][p2[1]][p2[0]]
            self.labirint['spawn_target'].append((p1 if p2_grp == start_grp else p2, (x, y)))
        else:
            x, y = (randint(0, self.labirint['cols'] - 1), randint(0, self.labirint['rows'] - 1))
            while self.labirint['groups'][y][x] != start_grp:
                x, y = (randint(0, self.labirint['cols'] - 1), randint(0, self.labirint['rows'] - 1))
            self.labirint['buttons'].append([x, y, index])
            
            self.labirint['spawn_target'].append((start_pos, (x, y)))
            p2_grp = self.labirint['groups'][p2[1]][p2[0]]
            self.labirint['spawn_target'].append((p1 if p2_grp == start_grp else p2, finish_pos))
                
        
        
    def find_path(self, pos, old_val, new_val):
        query = [pos]
        i = 0
        while len(query) > i:
            x, y = query[i]
            self.labirint['groups'][y][x] = new_val
            if not self.labirint['verticals'][y + 1][x + 1] and old_val == self.labirint['groups'][y][x + 1]:
                query.append([x + 1, y])
            if not self.labirint['verticals'][y + 1][x] and old_val ==  self.labirint['groups'][y][x - 1]:
                query.append([x - 1, y])
            if not self.labirint['horizonts'][y + 1][x + 1] and old_val ==  self.labirint['groups'][y + 1][x]:
                query.append([x, y + 1])
            if not self.labirint['horizonts'][y][x + 1] and old_val ==  self.labirint['groups'][y - 1][x]:
                query.append([x, y - 1])
            i += 1

    def store_level(self, file_name=None):
        if file_name is None:
            pprint(self.labirint)
        else:
            with open(file_name, 'w') as level_file:
                json.dump(self.labirint, level_file)
                
    def load_level(self, file_name):
        with open(file_name, 'r') as level_file:
            return json.load(level_file)
    
if __name__ == '__main__':
    Labirint(8, 10).get_labirint()