inputs = []

while True:
    try:
        text = input()
    except EOFError as ex:
        break
    inputs.append(text)

# print('\n'.join(inputs))

cubes = set()

min_x_y_z = [999, 999, 999]
max_x_y_z = [0, 0, 0]

for line in inputs:
    x, y, z = [int(x) for x in line.split(',')]
    cubes.add((x,y,z))
    min_x_y_z[0], min_x_y_z[1], min_x_y_z[2] = min(min_x_y_z[0], x), min(min_x_y_z[1], y), min(min_x_y_z[2], z)
    max_x_y_z[0], max_x_y_z[1], max_x_y_z[2] = max(max_x_y_z[0], x), max(max_x_y_z[1], y), max(max_x_y_z[2], z)


def scan_cubes(cubes):
    total = 0
    def is_exist(x, y, z):
        return 0 if (x,y,z) in cubes else 1

    def scan(x, y, z):
        return is_exist(x+1 ,y, z) + is_exist(x-1, y, z) + \
                is_exist(x, y+1, z) + is_exist(x, y-1, z) + \
                is_exist(x, y, z+1) + is_exist(x, y, z-1)
                
    for x,y,z in list(cubes):
        total += scan(x, y, z)

    return total

# def is_exist(x, y, z):
#     return 0 if (x,y,z) in cubes else 1

# def scan(x, y, z):
#     return is_exist(x+1 ,y, z) + is_exist(x-1, y, z) + \
#             is_exist(x, y+1, z) + is_exist(x, y-1, z) + \
#             is_exist(x, y, z+1) + is_exist(x, y, z-1)
            
total = scan_cubes(cubes)

# for x,y,z in cubes.keys():
#     total += scan(x, y, z)

print(f'18.1: {total}')

total_cubes = (max_x_y_z[0]-min_x_y_z[0]+1)*(max_x_y_z[1]-min_x_y_z[1]+1)*(max_x_y_z[2]-min_x_y_z[2]+1)
# print(min_x_y_z)
# print(max_x_y_z)
print('total cubes', total_cubes)

# scan all cubes inside the area
outside_air = set()
global_visits = set()
trapped_cubes = []

for z in range(min_x_y_z[2], max_x_y_z[2]+1):
    for y in range(min_x_y_z[1], max_x_y_z[1]+1):
        for x in range(min_x_y_z[0], max_x_y_z[0]+1):
            if (x, y, z) in cubes or \
                (x, y, z) in global_visits:
                continue

            # do the bfs
            is_outside = False
            coords = [(x, y, z)]
            nodes = [(x, y, z)]
            nexts = set()
            visits = set()

            def is_connect_outside(cx, cy, cz):
                return cx + 1 > max_x_y_z[0] or cx - 1 < min_x_y_z[0] or \
                    cy + 1 > max_x_y_z[1] or cy - 1 < min_x_y_z[1] or \
                    cz + 1 > max_x_y_z[2] or cz - 1 < min_x_y_z[2]

            def check_coord(cx, cy, cz, dx=0, dy=0, dz=0):
                outside = False
                if dx != 0:
                    limit = max_x_y_z[0] if dx > 0 else min_x_y_z[0]
                    outside = cx+dx > limit if dx > 0 else cx+dx < min_x_y_z[0]
                if dy != 0:
                    limit = max_x_y_z[1] if dy > 0 else min_x_y_z[1]
                    outside = cy+dy > limit if dy > 0 else cy+dy < min_x_y_z[1]
                if dz != 0:
                    limit = max_x_y_z[2] if dz > 0 else min_x_y_z[2]
                    outside = cz+dz > limit if dz > 0 else cz+dz < min_x_y_z[2]
                    
                if (cx+dx, cy+dy, cz+dz) in cubes or \
                    (cx+dx, cy+dy, cz+dz) in global_visits or \
                    outside:
                    return False
                return True
                    
            while nodes:
                sx, sy, sz = nodes.pop(0)

                if (sx, sy, sz) not in global_visits:
                    visits.add((sx, sy, sz))
                    global_visits.add((sx, sy, sz))
                    
                    if check_coord(sx, sy, sz, dx=1):
                        nexts.add((sx+1, sy, sz))
                    if check_coord(sx, sy, sz, dx=-1):
                        nexts.add((sx-1, sy, sz))
                    if check_coord(sx, sy, sz, dy=1):
                        nexts.add((sx, sy+1, sz))
                    if check_coord(sx, sy, sz, dy=-1):
                        nexts.add((sx, sy-1, sz))
                    if check_coord(sx, sy, sz, dz=1):
                        nexts.add((sx, sy, sz+1))
                    if check_coord(sx, sy, sz, dz=-1):
                        nexts.add((sx, sy, sz-1))

                    is_outside = is_outside or is_connect_outside(sx, sy, sz)
                    
                    # print('visits', visits)
                    # print(nexts)
                    # print()

                if not nodes and nexts:
                    nodes = list(nexts)
                    nexts = set()

            # print(is_outside, visits)
            # print(visits)
            if is_outside:
                for sx, sy, sz in list(visits):
                    outside_air.add((sx, sy, sz))
            else:
                tc = set()
                for sx, sy, sz in list(visits):
                    tc.add((sx, sy, sz))
                trapped_cubes.append(tc)

assert len(cubes.intersection(outside_air)) == 0

no_of_trapped_cubes = sum([len(x) for x in trapped_cubes])
print('cubes', len(cubes))
print('outside_air', len(outside_air))
print('trapped cubes', no_of_trapped_cubes)

assert total_cubes == len(cubes) + len(outside_air) + no_of_trapped_cubes 
# print()
for tc in trapped_cubes:
    total -= scan_cubes(tc)
    # print('trapped_cubes', tc)
print(f'18.2: {total}')