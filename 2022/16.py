inputs = []

while True:
    try:
        text = input()
    except EOFError as ex:
        break
    inputs.append(text)

# print('\n'.join(inputs))

valves = {}
for line in inputs:
    txt = line.split()
    valve = txt[1]
    nexts = [t.strip(',') for t in txt[9:]]
    valves[valve] = {
        'valve': valve,
        'nexts': set(nexts),
        'rate': int(txt[4].strip(';').split('=')[1]),
    }
    # print(valves[valve])

start = 'AA'
budget = 30

targets = sorted([v for v in valves.values() if v['rate'] > 0], key=lambda x: x['rate'])
visits = set()

def find_dist(valves, start, end) -> int:
    nodes = [start]
    nexts = set()
    visits = set()
    dist = 0
    while nodes:
        n = nodes.pop(0)
        for next in list(valves[n]['nexts']):
            if next == end:
                return dist+1
            elif next in visits:
                continue
            nexts.add(next)
        if not nodes and nexts:
            nodes = list(nexts)
            nexts = set()
            dist += 1
    
    return dist

def search(valves, targets, current, budget, visits: set, opened, pressure):
    if budget <= 0:
        print(f'pressure: {pressure}, opened: {opened}')
        return

    current_opened = opened
    current_p = pressure
    
    # print(opened)
    
    for t in targets:
        v = t['valve']
        if v in visits:
            continue
        
        # bfs for distance
        # dist = find_dist(valves, current, v)
        # print(f'dist from {current} -> {v}')
        dist = valves[current][v]
        
        # open valve
        if dist + 1 < budget:
            p = (budget-dist-1) * t['rate']
            visits.add(v)
            
            result_p, result_opened = search(valves, targets, v, budget-dist-1, visits, opened+[v], pressure+p)
            if result_p > current_p:
                current_p, current_opened = result_p, result_opened
                
            visits.remove(v)
        
    return (current_p, current_opened)

# create direct tunnel
for t in targets:
    v = t['valve']
    for t2 in targets:
        v2 = t2['valve']
        if v == v2:
            continue
        
        dist = find_dist(valves, v, v2)
        
        valves[v][v2] = dist
        valves[v2][v] = dist

    dist = find_dist(valves, 'AA', v)
    valves[v]['AA'] = dist
    valves['AA'][v] = dist

print(len(targets))
for t in targets:
    print(t)

print()
    
p, opened = search(valves, targets, 'AA', 30, visits, [], 0)

print(f'16.1: pressure: {p}, opened: {opened}')

visits = set()

p, opened = search(valves, targets, 'AA', 26, visits, [], 0)

for o in opened:
    visits.add(o)

p2, opened2 = search(valves, targets, 'AA', 26, visits, [], 0)

print(f'16.2: pressure: {p+p2}, opened: {opened2+opened}')
