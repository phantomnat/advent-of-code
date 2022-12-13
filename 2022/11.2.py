inputs = []

while True:
    try:
        text = input()
    except EOFError as ex:
        break
    inputs.append(text)

# print('\n'.join(inputs))
monkeys = []

for i in range(0, len(inputs), 7):
    items = inputs[i+1].strip().split(' ')
    ops = inputs[i+2].strip().split(' ')
    tests = inputs[i+3].strip().split(' ')
    trues = inputs[i+4].strip().split(' ')
    falses = inputs[i+5].strip().split(' ')
    
    monkey = {
        'id': i//7,
        'items': [int(i.strip(',')) for i in items[2:]],
        'nexts': [],
        'ops': ops[3:],
        'test': int(tests[-1]),
        'true': int(trues[-1]),
        'false': int(falses[-1]),    
        'inspect': 0,
    }
    monkeys.append(monkey)

modulo = 1
for k in range(len(monkeys)):
    modulo *= monkeys[k]['test']

for i in range(10000):
    
    for j in range(len(monkeys)):
        testV = monkeys[j]['test']
        trueM = monkeys[j]['true']
        falseM = monkeys[j]['false']
        ops = monkeys[j]['ops']

        while monkeys[j]['items']:
            item = monkeys[j]['items'].pop(0)
            monkeys[j]['inspect']+=1
            wlv = item
            if ops[1] == '*':
                if ops[2] == 'old':
                    wlv *= item
                else:
                    wlv *= int(ops[2])
            elif ops[1] == '+':
                if ops[2] == 'old':
                    wlv += item
                else:
                    wlv += int(ops[2])
                    
            # wlv //= 3
            
            if wlv % testV == 0:
                monkeys[trueM]['items'].append(wlv%modulo)
            else:
                monkeys[falseM]['items'].append(wlv%modulo)

sortedMonkeys = sorted(monkeys, key=lambda x: (-x['inspect']))[:2]
print(sortedMonkeys[0]['inspect']*sortedMonkeys[1]['inspect'])
