inputs = []

while True:
    try:
        text = input()
    except EOFError as ex:
        break
    inputs.append(text)

crt_pos = 1
value = 1
crt = ['.']*240

instructions = []

for line in inputs:
    if line == 'noop':
        instructions.append(('noop'))
    else:
        instructions.append(('noop'))

        cmd, val = line.split(' ')
        val = int(val)
        
        instructions.append((val, val))

cycle = 1

for inst in instructions:
    if value <= crt_pos%40 and crt_pos%40 <= value+2:
        crt[crt_pos-1] = '#'
    
    print(f'sprite: {value}, crt: {crt_pos}')
    crt_pos += 1
    
    
    for i in range(0, 241, 40):
        print(''.join(crt[i:i+40]))
    print()

    if len(inst) == 2:
        value += inst[0]

    cycle += 1