scores = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}
incomplete_scores = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4,
}

error_score = 0
invalid_scores = []

while True:
    try:
        text = input()
    except EOFError as ex:
        break
    
    stack = []
    corrupt = False
    
    for c in list(text):
        if c in {'{', '[', '(', '<'}:
            stack.append(c)
        else:
            # if len(stack) == 0:
            #     # ignore
            #     break
            
            last = stack.pop()
            if (last == '(' and c != ')') or (last == '[' and c != ']') or (last == '{' and c != '}') or (last == '<' and c != '>'):
                error_score += scores[c]
                corrupt = True
                break

    if corrupt:
        continue
    
    print(stack)
    score = 0
    while stack:
        c = stack.pop()
        
        score *= 5
        score += incomplete_scores[c]
    
    print(score)
    invalid_scores.append(score)    
    
print(f'error score: {error_score}')

sorted_invalid_scores = sorted(invalid_scores)
print(sorted_invalid_scores[len(sorted_invalid_scores)//2])