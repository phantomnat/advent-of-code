inputs = []

while True:
    try:
        text = input()
    except EOFError as ex:
        break
    inputs.append(text)

# print('\n'.join(inputs))

terrain = []
start_pt = ()
end_pt = ()

for y, line in enumerate(inputs):
    t = []
    for x, c in enumerate(list(line)):
        if ord('a') <= ord(c) and ord('z') >= ord(c):
            t.append(ord(c) - ord('a'))
        elif c == 'S':
            t.append(0)
            start_pt = (x, y)
        else:
            t.append(ord('z')-ord('a'))
            end_pt = (x, y)
    
    terrain.append(t)

print(f'start: {start_pt}')
print(f'end  : {end_pt}')

# for t in terrain:
#     print(t)

h = len(terrain)
w = len(terrain[0])
distance = [[w*h for _ in range(w)] for _ in range(h)]

dist = 0
nodes = [end_pt]
nexts = set()
visits = set()

def calc_elevation(terrain: list, x: int, y: int, w: int, h: int, visits: set, nexts: set):
    current_elv = terrain[y][x]
    
    def can_step_up_or_down(x2: int, y2: int) -> bool:
        # step up
        if current_elv > terrain[y2][x2]:
            return current_elv - terrain[y2][x2] <= 1
        # step down
        return True

    can_step_right = x+1 < w and (x+1, y) not in visits
    can_step_left = x-1 >= 0 and (x-1, y) not in visits
    can_step_up = y-1 >= 0 and (x, y-1) not in visits
    can_step_down = y+1 < h and (x, y+1) not in visits
    
    if can_step_right and can_step_up_or_down(x+1, y):
        nexts.add((x+1, y))
    if can_step_left and can_step_up_or_down(x-1, y):
        nexts.add((x-1, y))
    if can_step_up and can_step_up_or_down(x, y-1):
        nexts.add((x, y-1))
    if can_step_down and can_step_up_or_down(x, y+1):
        nexts.add((x, y+1))

while nodes:
    px, py = nodes.pop(0)
    
    visits.add((px, py))
    current_lv = terrain[py][px]
    distance[py][px] = min(distance[py][px], dist)
    
    calc_elevation(terrain, px, py, w, h, visits, nexts)

    if not nodes:
        # print(nexts)
        nodes = list(nexts)
        nexts = set()
        dist += 1

print(f'12.1: {distance[start_pt[1]][start_pt[0]]}')

min_dist = w*h

for y in range(h):
    for x in range(w):
        if terrain[y][x] == 0:
            min_dist = min(min_dist, distance[y][x])
print(f'12.2: {min_dist}')