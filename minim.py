import operator
import re
import sys

# minim 
# by las-r

# constants
TOKENREGEX = r"'[^']*'|\{|\||\}|\S+"
OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "%": operator.mod,
    "&": operator.and_,
    "|": operator.or_,
    "^": operator.xor,
    "~": operator.invert,
    "==": lambda a, b: 1 if a == b else 0,
    ">": lambda a, b: 1 if a > b else 0,
    "<": lambda a, b: 1 if a < b else 0,
    ">=": lambda a, b: 1 if a >= b else 0,
    "<=": lambda a, b: 1 if a <= b else 0,
    "&&": lambda a, b: 1 if a != 0 and b != 0 else 0,
    "||": lambda a, b: 1 if a != 0 or b != 0 else 0,
    "^^": lambda a, b: 1 if (a != 0) != (b != 0) else 0,
}

# break exception
class Break(Exception):
    def __init__(self, val):
        self.val = val

# parser function
def parse(tokens):
    index = 0

    # peek helper
    def peek():
        if index < len(tokens):
            return tokens[index]
        return None

    # keyword parser
    def parsenext():
        nonlocal index
        if index >= len(tokens):
            return None
        
        tok = tokens[index]
        index += 1

        # parentheses
        if tok == "(":
            expr = parse_expr()
            if peek() == ")":
                index += 1
            return expr

        # set
        if tok == "set":
            if index >= len(tokens):
                return None
            name = tokens[index]
            index += 1
            val = parse_expr()
            return SetNode(name, val)

        # input
        if tok == "in":
            msg = parse_expr()
            return InputNode(msg)

        # print
        if tok == "out":
            val = parse_expr()
            return PrintNode(val)

        # num
        if tok == "num":
            val = parse_expr()
            return NumNode(val)

        # loopif
        if tok == "loopif":
            cond = parse_expr()
            body = []
            if peek() == "{":
                index += 1
                while peek() != "}" and index < len(tokens):
                    node = parsenext()
                    if node:
                        body.append(node)
                if peek() == "}":
                    index += 1
            return LoopIfNode(cond, body)

        # break
        if tok == "break":
            val = parse_expr()
            return BreakNode(val)
        
        # literal and get
        try:
            return LiteralNode(float(tok))
        except ValueError:
            if len(tok) >= 2 and tok[0] == tok[-1] == "'":
                return LiteralNode(tok[1:-1])
            else:
                return GetNode(tok)

    # expression parser
    def parse_expr():
        nonlocal index
        a = parsenext()
        while peek() in OPS:
            tok = tokens[index]
            index += 1
            b = parsenext()
            a = OpNode(tok, a, b)
        return a

    # create tree
    nodes = []
    while index < len(tokens):
        node = parsenext()
        if node:
            nodes.append(node)
    return nodes

# nodes
class LiteralNode:
    def __init__(self, val):
        self.val = val
        
    def eval(self):
        return self.val

class GetNode:
    def __init__(self, name):
        self.name = name

    def eval(self):
        return env[self.name]

class SetNode:
    def __init__(self, name, val):
        self.name = name
        self.val = val

    def eval(self):
        env[self.name] = self.val.eval()
        return env[self.name]

class OpNode:
    def __init__(self, op, a, b):
        self.op = op
        self.a = a
        self.b = b
    
    def eval(self):
        return OPS[self.op](self.a.eval(), self.b.eval())

class InputNode:
    def __init__(self, msg):
        self.msg = msg

    def eval(self):
        return input(self.msg.eval())

class PrintNode:
    def __init__(self, val):
        self.val = val

    def eval(self):
        val = self.val.eval()
        print(val)
        return val

class NumNode:
    def __init__(self, val):
        self.val = val

    def eval(self):
        return float(self.val.eval())

class LoopIfNode:
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def eval(self):
        res = None
        while self.cond.eval() != 0:  
            for node in self.body:
                try:
                    res = node.eval()
                except Break as b:
                    if b.val is not None:
                        return b.val
                    else:
                        continue
        return res

class BreakNode:
    def __init__(self, val):
        self.val = val

    def eval(self):
        raise Break(self.val.eval())

# open file
if len(sys.argv) > 1:
    with open(sys.argv[1]) as f:
        code = f.read()
else:
    print("usage: python minim.py file_to_run.mn")
    sys.exit(1)

# execute
tokens = re.findall(TOKENREGEX, re.sub(r'#[^\n]*', '', code))
nodes = parse(tokens)
env = {}
for node in nodes:
    node.eval()