from tusan.lexer.Token import *

class Node:
    def __init__(self, type_, name, translation={}):
        self.name = name
        self.type = type_
        self.translation = {}

# okay now i realise this shit was from the prototype 3 months back