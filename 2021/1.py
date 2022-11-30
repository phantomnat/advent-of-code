# prev = None
count = 0
values = []
aggregates = []

while True:
    try:
        text = input()
    except EOFError as ex:
        break
    
    val = int(text)
    values.append(val)
    
    if aggregates:
        val += aggregates[-1]
    if len(values) > 3:
        val -= values[-4]
        
    aggregates.append(val)    
    
    if len(aggregates) > 3 and aggregates[-1] > aggregates[-2]:
        count += 1
    
print(count)