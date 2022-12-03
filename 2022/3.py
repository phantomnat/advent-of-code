score = 0

items = []

def get_score(same: set) -> int:
    score = 0
    for c in list(same):
        if c >= 'a' and c <= 'z':
            score += ord(c) - ord('a') + 1
        else:
            score += ord(c) - ord('A') + 27
    return score

while True:
    try:
        text = input()
    except EOFError as ex:
        break

    items.append(text)
    
    
    n = len(text)//2
    item1, item2 = text[:n], text[n:]

    
    print(item1, item2)
    
    same = set(item1).intersection(set(item2))
    
    score += get_score(same)
print(score)


total = 0

for i in range(0, len(items), 3):
    same = set(items[i]).intersection(set(items[i+1]), set(items[i+2]))
    print(same)
    total += get_score(same)
    
print(total)

    