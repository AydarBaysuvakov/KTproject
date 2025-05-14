class Bot:
    def __init__(self, labirint):
        self.labirint = labirint.copy()
        self.make_doors()
        self.path()
    
    def make_doors(self):
        for door in self.labirint['doors']:
            self.labirint[door[0]][door[1][0]][door[1][1]] = 1
            
    def get_way(self):
        return self.way
    
    def path(self):
        self.way = []
        self.rows, self.cols = self.labirint['rows'], self.labirint['cols']
        start = self.labirint['start']
        finish = self.labirint['finish']
        buttons = self.labirint['buttons']
        doors   = self.labirint['doors']
        for grp in self.labirint['spawn_target']:
            if grp[0] == start:
                target = grp[1]
                break
        
        while True:
            if start == target:
                return False
            self.explored = [[0 for i in range(self.cols)] for i in range(self.rows)]
            path = self.dfs(start, target)
            if path[0]:
                self.way += path
            else:
                return False
            if target == finish:
                return True
            
            found = False
            for i in range(len(buttons)):
                if (buttons[i][0], buttons[i][1]) == target:
                    start = target
                    door = doors[i]
                    self.labirint[door[0]][door[1][0]][door[1][1]] = 0
                    if door[0] == 'verticals':
                        for grp in self.labirint['spawn_target']:
                            if grp[0] == [door[1][1] - 1, door[1][0] - 1] or grp[0] == [door[1][1]    , door[1][0] - 1]:
                                if target == grp[1]:
                                    return False
                                target = grp[1]
                                found = True
                                break
                    elif door[0] == 'horizonts':
                        for grp in self.labirint['spawn_target']:
                            if grp[0] == [door[1][1] - 1, door[1][0] - 1] or grp[0] == [door[1][1] - 1, door[1][0]    ]:
                                if target == grp[1]:
                                    return False
                                target = grp[1]
                                found = True
                                break
            if not found:
                return False
        
    def dfs(self, start_pos, end_pos):
        if start_pos == end_pos:
            return (True, [end_pos])
        
        x, y = start_pos
        self.explored[y][x] = 1
        next = []
        if not self.labirint['verticals'][y + 1][x + 1] and not self.explored[y][x + 1]:
            next = self.dfs((x + 1, y), end_pos)
            if next[0]:
                return (True, [start_pos] + next[1]) 
        if not self.labirint['verticals'][y + 1][x] and not self.explored[y][x - 1]:
            next = self.dfs((x - 1, y), end_pos)
            if next[0]:
                return (True, [start_pos] + next[1]) 
        if not self.labirint['horizonts'][y + 1][x + 1] and not self.explored[y + 1][x]:
            next = self.dfs((x, y + 1), end_pos)
            if next[0]:
                return (True, [start_pos] + next[1]) 
        if not self.labirint['horizonts'][y][x + 1] and not self.explored[y - 1][x]:
            next = self.dfs((x, y - 1), end_pos)
            if next[0]:
                return (True, [start_pos] + next[1]) 
            
        return (False, [])

