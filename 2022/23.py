inputs = []

input_file = 'input/actual'
# input_file = 'input/example'
with open(input_file, 'r') as fp:
    inputs = fp.readlines()

top_l = [len(inputs), len(inputs)]
bot_r = [0, 0]
maps = {}
no_of_elves = 0

def expand(x, y, top_l, bot_r):
    top_l[0] = min(top_l[0], x)
    top_l[1] = min(top_l[1], y)
    bot_r[0] = max(bot_r[0], x)    
    bot_r[1] = max(bot_r[1], y)
    return top_l, bot_r
     
for y, line in enumerate(inputs):
    line = line.strip('\n')
    for x, c in enumerate(line):
        if c == '.':
            continue
        maps[(x, y)] = c
        # expand(x, y)
        no_of_elves += 1
        
def print_maps():
    top_l = [len(inputs), len(inputs)]
    bot_r = [0, 0]
    for x, y in maps.keys():
        top_l, bot_r = expand(x, y, top_l, bot_r)
    
    for y in range(top_l[1], bot_r[1]+1):
        line = ''
        for x in range(top_l[0], bot_r[0]+1):
            if (x, y) in maps:
                line += maps[(x, y)]
            else:
                line += '.'
        print(line)
    print()
    
directions = [
    ((0, -1), [(-1, -1), (0, -1), (1, -1)], '^'), # north
    ((0, 1), [(-1, 1), (0, 1), (1, 1)], 'v'), # south
    ((-1, 0), [(-1, -1), (-1, 0), (-1, 1)], '<'), # west
    ((1, 0), [(1, -1), (1, 0), (1, 1)], '>'), # east
]

def scan_elf(x, y, start_idx):
    is_move = False
    
    # scan 8
    for i in range(-1, 2): # -1 .. 1
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if (x+i, y+j) in maps:
                is_move = True
                break
        if is_move:
            break
    
    if is_move:
        for i in range(start_idx, start_idx+5): # start_idx .. start_idx+4
            is_found = False
            dir = directions[i%len(directions)]
            # print(f'({x}, {y}) scanning {dir[2]}')
            
            for dx, dy in dir[1]:
                if (x+dx, y+dy) in maps:
                    is_found = True
                    break

            if not is_found:
                # print(f'({x}, {y}) move {dir[2]}')
                return True, x+dir[0][0], y+dir[0][1]

    # print(f'({x}, {y}) is not move')
    return False, 0, 0

verbose = True
verbose = False
   
def next_step(round):
    next_pos_to_elf = {}
    # scan
    for x, y in maps.keys():
        is_move, nx, ny = scan_elf(x, y, round)
        if not is_move:
            continue
        if (nx, ny) not in next_pos_to_elf:
            next_pos_to_elf[(nx, ny)] = set()
        next_pos_to_elf[(nx, ny)].add((x, y))
    
    # if verbose:
    #     for nx, ny in next_pos_to_elf.keys():
    #         print(f'{next_pos_to_elf[(nx, ny)]} -> ({nx}, {ny})')
    
    no_elf_moved = True
    
    # move
    for nx, ny in next_pos_to_elf.keys():
        if len(next_pos_to_elf[(nx, ny)]) > 1:
            continue
        ox, oy = list(next_pos_to_elf[(nx, ny)])[0]
        # assert (ox, oy) in maps
        maps.pop((ox, oy), None)
        # maps[(ox, oy)] = '.'
        maps[(nx, ny)] = '#'
        no_elf_moved = False

    if verbose:
        print('round', round+1)
        print_maps()

    return no_elf_moved

round = 0
while round < 10:
    next_step(round)
    round += 1

for x, y in maps.keys():
    top_l, bot_r = expand(x, y, top_l, bot_r)

p1_ans = ((bot_r[0] - top_l[0] + 1) * (bot_r[1] - top_l[1]+1)) - no_of_elves
# print_maps()
print('no of elves', no_of_elves)
print('top left:', top_l, ', bot right:', bot_r)
print(f'23.1: {p1_ans}')

# round = 10
while not next_step(round):
    round += 1
# print_maps()
print(f'23.2: {round+1}')
