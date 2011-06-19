#!/usr/bin/env python
import budget

bud = budget.load_budget( "./" )

for b in bud:
    print b.name, b.cost

