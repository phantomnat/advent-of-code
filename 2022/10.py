inputs = []

while True:
    try:
        text = input()
    except EOFError as ex:
        break
    inputs.append(text)

# print('\n'.join(inputs))

cycle = 1
value = 1

total = 0
next_40 = 0
last_inst_cycle = 0
inst_cycle = 1

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
    
    
    if cycle == (20+(40*next_40)):
        signal = (20+(40*next_40))
        print(f'{signal}th * {value}')
        next_40 += 1
        total += signal*value
    
    if len(inst) == 2:
        value += inst[0]
    else:
        pass
    
    print(f'cycle: {cycle} = {value}')
    cycle += 1
        
    
print(f'instructions: {len(instructions)}')

print(total)
