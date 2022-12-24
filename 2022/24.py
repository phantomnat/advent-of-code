inputs = []

input_file = 'input/actual'
# input_file = 'input/example'
with open(input_file, 'r') as fp:
    inputs = fp.readlines()

maps = {}
blizzards = {}
dir_to_diff = {
    '^': (0, -1),
    'v': (0, 1),
    '<': (-1, 0),
    '>': (1, 0),
}
start = None
end = None

for y, line in enumerate(inputs):
    line = line.strip('\n')
    for x, c in enumerate(line):
        # maps[(x, y)] = c
        if c in dir_to_diff:
            blizzards[(x, y)] = [(c, dir_to_diff[c])]
        elif c == '#':
            maps[(x, y)] = c

        if start is None and y == 0 and c == '.':
            start = (x, y)
        if end is None and y == len(inputs)-1 and c == '.':
            end = (x, y)

def expand(x, y, top_l, bot_r):
    top_l[0] = min(top_l[0], x)
    top_l[1] = min(top_l[1], y)
    bot_r[0] = max(bot_r[0], x)    
    bot_r[1] = max(bot_r[1], y)
    return top_l, bot_r

def print_maps(step, blizzards, nexts):
    top_l = [len(inputs), len(inputs)]
    bot_r = [0, 0]
    for x, y in maps.keys():
        top_l, bot_r = expand(x, y, top_l, bot_r)
    
    # h = bot_r[1] - top_l[1] + 1
    # w = bot_r[0] - top_l[0] + 1
    # print('h', h, 'w', w)
    print('step', step)
    for y in range(top_l[1], bot_r[1]+1):
        line = ''
        for x in range(top_l[0], bot_r[0]+1):
            if (x, y) in maps:
                line += maps[(x, y)]
            elif (x, y) in blizzards:
                bs = blizzards[(x, y)]
                if len(bs) == 1:
                    line += bs[0][0]
                else:
                    line += str(len(bs))
            elif (x, y) in nexts:
                line += 'O'
            else:
                line += ' '
        print(line)
    print()

def go_opposite(x, y, dx=0, dy=0):
    nx, ny = x, y
    while (nx+dx, ny+dy) not in maps:
        nx += dx
        ny += dy
    assert (nx+dx, ny+dy) in maps and maps[(nx+dx, ny+dy)] == '#'
    return nx, ny

print('start', start, 'end', end)
# print('blizzards', blizzards)
# print_maps(0, blizzards, set(start))

def run_step(blizzards):
    new_blizzards = {}
    
    for x, y in blizzards.keys():
        bs = blizzards[(x, y)]
        for c, diff in bs:
            dx, dy = diff
            np = (x+dx, y+dy)
            if np in maps and maps[np] == '#':
                np = go_opposite(x, y, dx*-1, dy*-1)
            
            if np not in new_blizzards:
                new_blizzards[np] = []
                
            new_blizzards[np].append((c, diff))

    return new_blizzards
    
top_l = [len(inputs), len(inputs)]
bot_r = [0, 0]
for x, y in maps.keys():
    top_l, bot_r = expand(x, y, top_l, bot_r)

def walk(start, end, blizzards):
    finish = False
    step = 0
    nodes = [start]
    nexts = set()
    
    while not finish:
        blizzards = run_step(blizzards)
        
        for pos in nodes:
            x, y = pos
            left = (x-1, y)
            right = (x+1, y)
            up = (x, y-1)
            down = (x, y+1)

            if pos == start:
                nexts.add(pos)
                if down not in blizzards and y+1 <= bot_r[1]:
                    nexts.add(down)
                if up not in blizzards and y-1 >= top_l[1]:
                    nexts.add(up)
                continue

            for np in [left, right, up, down]:
                if np == end:
                    return step+1, blizzards
                    
                if np not in maps and np not in blizzards:
                    nexts.add(np)

            if pos not in blizzards:
                nexts.add(pos)

        # print_maps(i+1, blizzards, nexts)
        nodes = list(nexts)
        nexts = set()
        step += 1

first, blizzards = walk(start, end, blizzards)

print('24.1', first)

second, blizzards = walk(end, start, blizzards)

print('second', second)

third, blizzards = walk(start, end, blizzards)

print('third', third)

print('24.2', first+second+third)