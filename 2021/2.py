x = 0
y = 0
angle = 0

while True:
    try:
        text = input()
    except EOFError as ex:
        break
    
    action, unit = text.split()
    
    if action == 'forward':
        x += int(unit)
        y += int(unit) * angle
    elif action == 'down':
        angle += int(unit)
    elif action == 'up':
        angle -= int(unit)
    
print(x*y)