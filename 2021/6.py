fish = [int(x) for x in input().split(',')]

fish_mem = {x: 0 for x in range(9)}
for f in fish:
    fish_mem[f] = fish_mem.get(f, 0)+1
    

def run(fish_mem: dict) -> dict:
    new_mem = {x: 0 for x in range(9)}
    
    for i in range(9):
        v = fish_mem[i]

        if v == 0:
            continue
        
        if i == 0:
            new_mem[8] = new_mem.get(8, 0)+v
            new_mem[6] = new_mem.get(6, 0)+v
        else:
            new_mem[i-1] = new_mem.get(i-1, 0)+v
            
    return new_mem

for i in range(80):
    fish_mem = run(fish_mem)
    
print(f'total fish after  80 days: {sum(fish_mem.values())}')

for i in range(80, 256):
    fish_mem = run(fish_mem)
    
print(f'total fish after 256 days: {sum(fish_mem.values())}')