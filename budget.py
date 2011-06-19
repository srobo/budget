"Library for accessing the budget files"
import yaml, sympy, os, sys, logging
from decimal import Decimal as D

class BudgetItem(object):
    def __init__(self, name, fname, conf):
        self.fname = fname
        y = yaml.load( open(fname, "r") )

        if False in [x in y for x in ["cost", "summary", "description"]]:
            print >>sys.stderr, "Error: %s does not match schema." % fname
            exit(1)

        self.name = name
        self.summary = y["summary"]
        self.description = y["description"]

        c = sympy.S( y["cost"] )
        self.cost = D( "%.2f" % c.evalf( subs = conf.vars ) )

class BudgetConfig(object):
    def __init__(self, fname):
        y = yaml.load( open(fname, "r") )

        if "vars" not in y:
            raise Exception("No variables declaration section in config")
        self.vars = y["vars"]

def load_budget(root):
    config_path = os.path.join( root, "config.yaml" )
    conf = BudgetConfig( config_path )
    budget = []

    for dirpath, dirnames, filenames in os.walk(root):
        try:
            dirnames.remove(".git")
            dirnames.remove(".meta")
        except ValueError:
            "Those directories will not always be there"
            pass

        for fname in filenames:
            fullp = os.path.join(dirpath, fname)
            if fullp == config_path:
                "The config file is a yaml file, but not a budget item"
                continue

            if fname[-5:] != ".yaml":
                continue

            name = fullp[:-5]
            if name[0] == ".":
                name = name[1:]

                if name[0] == "/":
                    name = name[1:]

            budget.append( BudgetItem(name, fullp, conf) )
    return budget
