create_lines = []

num_row = 8

for i in range(num_row):
    create_lines.append(list(input()))

numbers_idx = []

for i, c in enumerate(list(input())):
    if c != ' ':
        numbers_idx.append((ord(c)-ord('0'), i))

crates_stack = {row: [] for row, _ in numbers_idx}

# print(crates_stack)

for line in create_lines:
    for row, idx in numbers_idx:
        if line[idx] != ' ':
            crates_stack[row].append(line[idx])

# print(crates_stack)

input()

# print(numbers_idx)        

cmds = []
while True:
    try:
        text = input()
    except EOFError as ex:
        break
    
    cmds.append(text.split())

# print(cmds)  
  
for cmd, amount, _, _from, _, _to in cmds:
    amount = int(amount)
    _from = int(_from)
    _to = int(_to)
    
    print(f'{cmd} {amount} {_from} -> {_to}')
    
    froms = []
    
    i = 0
    for i in range(amount):
        froms.insert(0, crates_stack[_from].pop(0))
    for f in froms:
        crates_stack[_to].insert(0,f)
        
    # print(crates_stack)
    
chars = [stack[0] for idx, stack in crates_stack.items()]

print(''.join(chars))