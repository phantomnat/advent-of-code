
pairs = []

while True:
    try:
        text = input()
    except EOFError as ex:
        break

    p1, p2 = text.split(',')
    
    pairs.append((tuple(int(x) for x in p1.split('-')), tuple(int(x) for x in p2.split('-'))))
    
# print(pairs)

fully_contains = 0
overlaps = 0
for (x1, x2), (y1, y2) in pairs:
    # print(x1, x2, y1, y2)
    
    if ( x1 <= y1 and x2 >= y2) or (y1 <= x1 and y2 >= x2):
        fully_contains += 1
        overlaps += 1
    elif (x1 <= y1 and x2 >= y1) or (x1 <= y2 and x2 >= y2) or (y1 <= x1 and y2 >= x1) or (y1 <= x2 and y2 >= x2):
        overlaps += 1
        
print(fully_contains)

print(f'overlap: {overlaps}')