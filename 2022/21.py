inputs = []

input_file = 'input/actual'
# input_file = 'input/example'
with open(input_file, 'r') as fp:
    inputs = fp.readlines()
    
# print(inputs)

monkeys = {}
nodes = []
visits = set()
required_monkeys = {}

for line in inputs:
    arr = line.split()
    name = arr[0].strip(':')
    if len(arr) == 2:
        monkeys[name] = [int(arr[1])]
        nodes.append(name)
    else:
        m1, op, m2 = arr[1], arr[2], arr[3]
        if m1 not in required_monkeys:
            required_monkeys[m1] = set()
        if m2 not in required_monkeys:
            required_monkeys[m2] = set()
        required_monkeys[m1].add(name)
        required_monkeys[m2].add(name)
        monkeys[name] = [m1, op, m2]

nexts = set()
processed = []

# print(monkeys)

while nodes:
    name = nodes.pop(0) 
    
    # print(f'search: {name}')
    
    if len(monkeys[name]) == 3:
        # print(monkeys[name])
        m1, op, m2 = monkeys[name]
        assert m1 in visits and m2 in visits
        if op == '+':
            monkeys[name] =  [monkeys[m1][0] + monkeys[m2][0]]
        elif op == '-':
            monkeys[name] = [monkeys[m1][0] - monkeys[m2][0]]
        elif op == '*':
            monkeys[name] = [monkeys[m1][0] * monkeys[m2][0]]
        elif op == '/':
            monkeys[name] = [monkeys[m1][0] // monkeys[m2][0]]
        
    processed.append(name)
    visits.add(name)

    if not nodes:
        for p in processed:
            if p not in required_monkeys:
                continue

            for nm in list(required_monkeys[p]):
                if nm in visits or len(monkeys[nm]) == 1:
                    continue
                
                m1, _, m2 = monkeys[nm]
                if m1 in visits and m2 in visits:
                    # print(f'add {nm}')
                    nexts.add(nm)

        nodes = list(nexts)
        nexts = set()
        # print(nodes)
                
    # print(monkeys)
print(f'21.1: {monkeys["root"][0]}')

monkeys = {}

for line in inputs:
    arr = line.split()
    name = arr[0].strip(':')
    if len(arr) == 2:
        monkeys[name] = [int(arr[1])]
    else:
        m1, op, m2 = arr[1], arr[2], arr[3]
        monkeys[name] = [m1, op, m2]

# print(monkeys)

# dfs

def search(monkeys, name, solve=True):
    if len(monkeys[name]) == 1:
        if name == 'humn':
            return False, 'x'
        return True, monkeys[name][0]
    m1, op, m2 = monkeys[name]

    s1, v1 = search(monkeys, m1)
    s2, v2 = search(monkeys, m2)
    if s1 and s2:
        if op == '+':
            r = v1 + v2
        elif op == '-':
            r = v1 - v2
        elif op == '*':
            r = v1 * v2
        else:
            r = v1 // v2
        return True, r
    
    return False, f'({v1} {op} {v2})'


_, l = search(monkeys, monkeys['root'][0], True)
_, r = search(monkeys, monkeys['root'][2], True)
# print()
# print(l, '=', r)


if input_file == 'input/example':
    '''
    (2 * (x - 3)) = 150
    '''
    ans = (((150 * 4) - 4) // 2) + 3
else:
    def calc(x):
        return int(eval('(20 * (((7430909554588 - ((((((219 + (2 * (((((((((((599 + ((2 * (278 + (((2 * ((3 * (((569 + (((((135 + (((10 * (((446 + (2 * (((((((563 + ((((((((301 + (((((7 * (109 + ((116 + (343 + ((x - 838) * 17))) / 5))) - 797) + 909) / 2) + 636)) / 3) - 518) * 8) + 294) * 2) - 460) / 4)) / 3) - 159) * 5) - 282) / 2) + 297))) / 8) - 24)) - 930) / 2)) * 2) - 453) + 310) + 24)) / 5) + 350)) - 732)) + 711) / 3))) - 309)) / 6) - 300) / 12) + 825) * 67) - 458) / 2) + 400) * 2) - 869))) / 7) + 22) * 2) - 738) / 10)) / 4) + 358))'))
    
    def binary_search(target):
        l = 0
        r = calc(0)
        while l < r:
            m = (l+r) // 2
            v = calc(m)
            # print(target, v, m)
            if v == target:
                return m
            elif v < target:
                r = m-1
            else:
                l = m+1
        return l

    ans = binary_search(r)
    
    # for x in range(1000):
    #     print(x, calc(x))
    
    '''
    (20 * (((7430909554588 - ((((((219 + (2 * (((((((((((599 + ((2 * (278 + (((2 * ((3 * (((569 + (((((135 + (((10 * (((446 + (2 * (((((((563 + ((((((((301 + (((((7 * (109 + ((116 + (343 + ((x - 838) * 17))) / 5))) - 797) + 909) / 2) + 636)) / 3) - 518) * 8) + 294) * 2) - 460) / 4)) / 3) - 159) * 5) - 282) / 2) + 297))) / 8) - 24)) - 930) / 2)) * 2) - 453) + 310) + 24)) / 5) + 350)) - 732)) + 711) / 3))) - 309)) / 6) - 300) / 12) + 825) * 67) - 458) / 2) + 400) * 2) - 869))) / 7) + 22) * 2) - 738) / 10)) / 4) + 358)) = 12133706805700
    '''
    # (((((((((599 + ((2 * (278 + (((2 * ((3 * (((569 + (((((135 + (((10 * (((446 + (2 * (((((((563 + ((((((((301 + (((((7 * (109 + ((116 + (343 + ((x - 838) * 17))) / 5))) - 797) + 909) / 2) + 636)) / 3) - 518) * 8) + 294) * 2) - 460) / 4)) / 3) - 159) * 5) - 282) / 2) + 297))) / 8) - 24)) - 930) / 2)) * 2) - 453) + 310) + 24)) / 5) + 350)) - 732)) + 711) / 3))) - 309)) / 6) - 300) / 12) + 825) * 67) - 458) / 2) + 400)

    # r = ((((((((((((((12133706805700 * 20) - 358) * 4) - 7430909554588)*-1)*10)+738) // 2) - 22) * 7) - 219) // 2) + 869) // 2)
    
print(f'21.2: {ans}')


