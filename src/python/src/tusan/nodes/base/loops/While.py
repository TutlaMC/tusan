from tusk.node import Node
from tusk.token import Token
from tusk.nodes.condition import *
class WhileNode(Node):
    def __init__(self, token: Token):
        from tusk.interpreter import Interpreter
        from tusk.nodes.statement import StatementNode
        self.token = token
        self.interpreter = token.interpreter
        self.cpos = self.interpreter.pos # position of condition start
        self.ecpos = self.cpos # position at ENDSTRUCTURE

    async def create(self):
        from tusk.nodes.statement import StatementNode
        await self.check()
        
        fned = False
        internal_structure_count = 0
        while fned != True:
            nxt_tkn = self.interpreter.next_token()
            if nxt_tkn.type=="ENDSTRUCTURE":
                if internal_structure_count == 0:
                    self.ecpos = self.interpreter.pos
                    fned = True
                else:
                    internal_structure_count -= 1
            elif nxt_tkn.type == "STRUCTURE":
                internal_structure_count += 1
            else: 
                self.interpreter.next_token()
        self.interpreter.pos = self.cpos
        await self.check() # this is just to skip the condition   
        
        internal_structure_count = 0
        while self.end_done:
            nxt_tkn = self.interpreter.next_token()
            if nxt_tkn.type=="ENDSTRUCTURE":
                if internal_structure_count == 0:
                    await self.check()
                else:
                    internal_structure_count -= 1
            elif nxt_tkn.type == "STRUCTURE":
                internal_structure_count += 1
            else: 
                await StatementNode(nxt_tkn).create()

             # recheck the condition
        self.interpreter.pos = self.ecpos
        return self

    async def check(self):
        self.interpreter.pos = self.cpos
        condition = await ConditionNode(self.token).create()
        self.interpreter.expect_token("KEYWORD:do")
        self.end_done = condition.value
        return self