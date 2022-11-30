hmap = []
risk_lv = 0

while True:
    try:
        text = input()
    except EOFError as ex:
        break
    
    hmap.append([int(x) for x in list(text)])

h = len(hmap)
w = len(hmap[0])
visits = {}
basins = []

for y in range(len(hmap)):
    for x in range(len(hmap[0])):
        neightbors = []
        
        if hmap[y][x] == 9:
            visits[(x,y)] = True
            continue
        
        if y-1 >= 0:
            neightbors.append(hmap[y-1][x])
        if y+1 < h:
            neightbors.append(hmap[y+1][x])
        if x-1 >= 0:
            neightbors.append(hmap[y][x-1])
        if x+1 < w:
            neightbors.append(hmap[y][x+1])
        
        if hmap[y][x] < min(neightbors):
            risk_lv += hmap[y][x]+1
            # bfs
            if visits.get((x,y), False):
                continue

            basin_size = 0
            nodes = [(x, y)]
            nexts = []
            while nodes:
                tx, ty = nodes.pop(0)
                if not visits.get((tx, ty), False):
                    visits[(tx, ty)] = True
                    basin_size += 1
                    for nx, ny in [(tx, ty-1), (tx, ty+1), (tx-1, ty), (tx+1, ty)]:
                        if nx < 0 or nx >= w or ny < 0 or ny >= h or hmap[ny][nx] > 8:
                            continue
                        nexts.append((nx, ny))
                        
                if not nodes and nexts:
                    nodes, nexts = nexts, []
                    
            basins.append(basin_size)
                
            
            
print(hmap)
    
print(f'risk lv: {risk_lv}')
sorted_basins = sorted(basins, key=lambda x: -x)[:3]
print(sorted_basins)

largest_basin_mul = 1
for v in sorted_basins:
    largest_basin_mul *= v
print(largest_basin_mul)
