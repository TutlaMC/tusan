from tusan.Node import *
from tusan.nodes.expression import *


class ReturnNode(Node):
    def __init__(self, token:Token):
        self.interpreter = token.interpreter
        self.token = token

    async def create(self):
        self.interpreter.return_value = (await ExpressionNode(self.interpreter.next_token()).create()).value
        self.interpreter.end_found = True
        return self

        
