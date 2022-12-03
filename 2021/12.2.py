from dataclasses import dataclass
from typing import Set, Dict, List
from collections import defaultdict

@dataclass
class Node:
    Name: str
    Nexts: Set[str]
    IsSmall: bool

paths: Dict[str, Node] = {}

while True:
    try:
        text = input()
    except EOFError as ex:
        break
    
    
    p1, p2 = text.split('-')
    if p1 not in paths:
        is_small = p1 == p1.lower()
        paths[p1] = Node(p1, set(), is_small)
    if p2 not in paths:
        is_small = p2 == p2.lower()
        paths[p2] = Node(p2, set(), is_small)

    paths[p1].Nexts.add(p2)
    paths[p2].Nexts.add(p1)

    
print(paths)

def dfs(paths: Dict[str, Node], visits: dict, current: Node, current_paths: List[str], all_paths: set):
    if current.Name == 'end':
        p = tuple(current_paths)
        if p in all_paths:
            return
        all_paths.add(p)
        # print(p)
        return
    
    if current.IsSmall:
        visits[current.Name] += 1

    for nextName in current.Nexts:
        next = paths[nextName]
        has_twice_visit = max(visits.values()) >= 2
        # is_skip = (has_twice_visit and visits[nextName] > 0) or (not has_twice_visit and visits[nextName] > 1)
        if nextName == 'start':
            continue
        elif has_twice_visit and visits[nextName] >= 1:
            continue
        elif not has_twice_visit and visits[nextName] >= 2:
            continue
        
        dfs(paths, visits, next, current_paths+[nextName], all_paths)
    
    if current.IsSmall:
        visits[current.Name] -= 1

visits = defaultdict(lambda: 0)
all_paths = set()
dfs(paths=paths, visits=visits, current=paths['start'],current_paths=['start'], all_paths=all_paths)

print(len(all_paths))
# print(all_paths)