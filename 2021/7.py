positions = {}

for x in input().split(','):
    positions[int(x)] = positions.get(int(x), 0)+1

min_position = min(positions.keys())
max_position = max(positions.keys())
min_cost = None
dists = {}

for i in range(min_position, max_position+1):
    dists[i] = i
    if i > 0:
        dists[i] = i+dists[i-1]

for i in range(min_position, max_position+1):
    cost = 0
    
    for k, v in positions.items():
        if i == k:
            continue
        
        cost += dists[abs(i-k)]*v
        
    min_cost = cost if min_cost is None else min(min_cost, cost)

# print(f'min: {}')


# for k in positions.keys():
#     cost = 0
#     for k2, v2 in positions.items():
#         if k == k2:
#             continue
        
#         cost += (abs(k-k2)*v2)
#         # print(f'{k}-{k2}*{v} = {abs(k-k2)}*{v} = {abs(k-k2)*v}')
    
#     print(f'key: {k}, cost: {cost}')
    
#     min_cost = cost if min_cost is None else min(min_cost, cost)

print(f'min cost: {min_cost}')
# print(positions)