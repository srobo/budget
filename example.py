#!/usr/bin/env python
import sr.budget as budget

bud = budget.load_budget( "./" )

for b in bud.walk():
    print b.name, b.cost

