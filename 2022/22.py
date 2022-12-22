inputs = []

input_file = 'input/actual'
# input_file = 'input/example'
with open(input_file, 'r') as fp:
    inputs = fp.readlines()

maps = {}
directions = ['>', 'v', '<', '^']
c_to_dirs = {c: i for i, c in enumerate(directions)}
cur_pos = None
cur_dir = 0

edges = []
top_left = [1,1]
bot_right = [1,1]

for y, line in enumerate(inputs[:len(inputs)-2]):
    # print(line)
    line = line.strip('\n')
    # if y == 0:
    for x, c in enumerate(line):
        if c == ' ':
            # if x+1 < len(line) and line[x+1] != ' ':
                # edges.append((x+1, y+1))
            continue
        top_left[0] = min(top_left[0], x+1)
        top_left[1] = min(top_left[1], y+1)
        bot_right[0] = max(bot_right[0], x+1)
        bot_right[1] = max(bot_right[1], y+1)
        if cur_pos is None:
            cur_pos = [x+1, y+1]
        maps[(x+1, y+1)] = c
        # if x == len(line)-1:
        #     edges.append((x+2, y+1))

print('start', cur_pos)
# print('top left', top_left)
# print('bot right', bot_right)

def print_maps(p1 = None, p2 = None, dir1 = 0, dir2 = 0):
    for y in range(1, bot_right[1]+1):
        line = ''
        for x in range(1, bot_right[0]+1):
            if p1 is not None and p1[0] == x and p1[1] == y:
                line += directions[dir1]
            elif p2 is not None and p2[0] == x and p2[1] == y:
                line += directions[dir2]
            elif (x, y) in maps:
                line += maps[(x,y)]
            else:
                line += ' '
        print(line)
    print('='*bot_right[0])

# print_maps()

import re
path = inputs[-1]

num_paths = re.split(r'[LR]', path)
dir_paths = re.split(r'[0-9]+', path)
paths = []
for i in range(len(num_paths)-1):
    paths.append(int(num_paths[i]))
    paths.append(dir_paths[i+1])
paths.append(int(num_paths[len(num_paths)-1]))

# print(num_paths)
# print(paths)
# print(path)

def turn(dir, c):
    if c == 'L':
        return (dir-1) % len(directions)
    else:
        return (dir+1) % len(directions)

def find_other_side(pos, dx=0, dy=0):
    nx, ny = pos
    while (nx+dx, ny+dy) in maps:
        nx += dx
        ny += dy
    assert (nx, ny) in maps
    return nx, ny
            
            
def step(dir, pos):
    dx, dy = 0, 0
    if directions[dir] == '>':
        dx = 1
    elif directions[dir] == '<':
        dx = -1
    elif directions[dir] == '^':
        dy = -1
    else:
        dy = 1

    np = (pos[0]+dx, pos[1]+dy)
    
    if (pos[0]+dx, pos[1]+dy) not in maps:
        np = find_other_side(pos, dx*-1, dy*-1)
        # print('direction', directions[dir])
        # print_maps(pos, np)

    if np in maps and maps[np] == '#':
        return True, pos

    return False, np

print(f'total steps: {len(paths)}')
assert ''.join([str(x) for x in paths]) == path

# print(paths)
p1_pos = cur_pos[:]
for i in range(len(paths)):
    if i%2 == 0:
        # walk into dir
        # from_pos = p1_pos[:]
        for s in range(paths[i]):
            is_stop, p1_pos = step(cur_dir, p1_pos)
            if is_stop:
                break
        # to_pos = p1_pos[:]
        # print('step', i+1, ':', paths[i], directions[cur_dir], from_pos, '->', to_pos)
    else:
        from_dir = cur_dir
        cur_dir = turn(cur_dir, paths[i])
        to_dir = cur_dir
        # print('step', i+1, ':', paths[i], directions[from_dir], directions[to_dir])
    # print_maps()
    # print()

# print_maps()
# print(cur_pos)
# print()
result = (p1_pos[1] * 1000) + (p1_pos[0]*4) + cur_dir
print(p1_pos, cur_dir)
print(f'22.1: {result}')

cube_width = 4 if input_file == 'input/example' else 50

def step_in_cube(dir, pos):
    dx, dy = 0, 0
    if directions[dir] == '>':
        dx = 1
    elif directions[dir] == '<':
        dx = -1
    elif directions[dir] == '^':
        dy = -1
    else:
        dy = 1

    np = (pos[0]+dx, pos[1]+dy)
    ndir = dir
    if (pos[0]+dx, pos[1]+dy) not in maps:
        # determine region
        region = 1
        if pos[0] <= cube_width:
            region = 2
        elif pos[0] > cube_width and pos[0] <= cube_width*2:
            region = 3
        elif pos[1] > cube_width*2:
            region = 5 if pos[0] <= cube_width*3 else 6
        elif pos[1] > cube_width and pos[1] <= cube_width*2 and pos[0] > cube_width*2:
            region = 4
        
        norm_regions = {
            1: (2, 0),
            2: (0, 1),
            3: (1, 1),
            4: (2, 1),
            5: (2, 2),
            6: (3, 2),
        }
        
        cube_x, cube_y = pos[0] - (norm_regions[region][0]*cube_width), pos[1] - (norm_regions[region][1]*cube_width)
        opposite_y = cube_width-cube_y+1
        opposite_x = cube_width-cube_x+1
        
        region_to_region = {
            (1, '<'): (3, 'v', (cube_y, 1)),
            (1, '^'): (2, 'v', (opposite_x, 1)),
            (1, '>'): (6, '<', (cube_width, opposite_y)),
            (2, '<'): (6, '^', (opposite_y, cube_width)),
            (2, '^'): (1, 'v', (opposite_x, 1)),
            (2, 'v'): (5, '^', (opposite_x, cube_width)),
            (3, '^'): (1, '>', (1, cube_x)),
            (3, 'v'): (5, '>', (1, opposite_x)),
            (4, '>'): (6, 'v', (opposite_y, 1)),
            (5, '<'): (3, '^', (opposite_y, cube_width)),
            (5, 'v'): (2, '^', (opposite_x, cube_width)),
            (6, '^'): (4, '<', (cube_width, opposite_x)),
            (6, '>'): (1, '<', (cube_width, opposite_y)),
            (6, 'v'): (2, '>', (1, opposite_x)),
        }
        
        assert (region, directions[dir]) in region_to_region
        rtr = region_to_region[(region, directions[dir])]
        ndir = c_to_dirs[rtr[1]]
        
        np = (rtr[2][0]+(norm_regions[rtr[0]][0]*cube_width), rtr[2][1]+(norm_regions[rtr[0]][1]*cube_width))
        
        # print('from', (region, directions[dir]), pos, 'to', rtr, np)
      
    if np in maps and maps[np] == '#':
        return True, pos, dir

    return False, np, ndir

def step_in_cube_actual(dir, pos):
    dx, dy = 0, 0
    if directions[dir] == '>':
        dx = 1
    elif directions[dir] == '<':
        dx = -1
    elif directions[dir] == '^':
        dy = -1
    else:
        dy = 1

    np = (pos[0]+dx, pos[1]+dy)
    ndir = dir
    if (pos[0]+dx, pos[1]+dy) not in maps:
        # determine region
        region = 1
        if pos[1] > cube_width and pos[1] <= cube_width*2:
            region = 3
        elif pos[1] > cube_width*3:
            region = 6
        elif pos[0] > cube_width*2:
            region = 2
        elif pos[1] > cube_width*2 and pos[1] <= cube_width*3:
            region = 4 if pos[0] <= cube_width else 5
        
        norm_regions = {
            1: (1, 0),
            2: (2, 0),
            3: (1, 1),
            4: (0, 2),
            5: (1, 2),
            6: (0, 3),
        }
        
        cube_x, cube_y = pos[0] - (norm_regions[region][0]*cube_width), pos[1] - (norm_regions[region][1]*cube_width)
        opposite_y = cube_width-cube_y+1

        region_to_region = {
            (1, '<'): (4, '>', (1, opposite_y)),
            (1, '^'): (6, '>', (1, cube_x)),
            (2, '^'): (6, '^', (cube_x, cube_width)),
            (2, '>'): (5, '<', (cube_width, opposite_y)),
            (2, 'v'): (3, '<', (cube_width, cube_x)),
            (3, '<'): (4, 'v', (cube_y, 1)),
            (3, '>'): (2, '^', (cube_y, cube_width)),
            (4, '^'): (3, '>', (1, cube_x)),
            (4, '<'): (1, '>', (1, opposite_y)),
            (5, '>'): (2, '<', (cube_width, opposite_y)),
            (5, 'v'): (6, '<', (cube_width, cube_x)),
            (6, '<'): (1, 'v', (cube_y, 1)),
            (6, '>'): (5, '^', (cube_y, cube_width)),
            (6, 'v'): (2, 'v', (cube_x, 1)),
        }
        
        assert (region, directions[dir]) in region_to_region
        
        rtr = region_to_region[(region, directions[dir])]
        ndir = c_to_dirs[rtr[1]]
        
        np = (rtr[2][0]+(norm_regions[rtr[0]][0]*cube_width), rtr[2][1]+(norm_regions[rtr[0]][1]*cube_width))
        
    if np in maps and maps[np] == '#':
        return True, pos, dir

    return False, np, ndir

p2_pos = cur_pos[:]
p2_dir = 0
p2_verbose = True
p2_verbose = False
for i in range(len(paths)):
    if i%2 == 0:
        # walk into dir
        if p2_verbose:
            from_pos = p2_pos[:]
        for s in range(paths[i]):
            if input_file == 'input/example':
                is_stop, p2_pos, p2_dir = step_in_cube(p2_dir, p2_pos)
            else:
                is_stop, p2_pos, p2_dir = step_in_cube_actual(p2_dir, p2_pos)
                

            if is_stop:
                break
        if p2_verbose:
            to_pos = p2_pos[:]
            print('step', i+1, ':', paths[i], directions[p2_dir], from_pos, '->', to_pos)
    else:
        if p2_verbose:
            from_dir = p2_dir
        p2_dir = turn(p2_dir, paths[i])
        if p2_verbose:
            to_dir = p2_dir
            print('step', i+1, ':', paths[i], directions[from_dir], directions[to_dir])
    if p2_verbose:
        print_maps(p1=p2_pos, dir1 = p2_dir)
    # print()

print(p2_pos, p2_dir)
result = (p2_pos[1] * 1000) + (p2_pos[0]*4) + p2_dir
print(f'22.2: {result}')