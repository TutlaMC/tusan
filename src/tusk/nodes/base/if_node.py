from tusk.node import Node
from tusk.token import Token
from tusk.nodes.condition import *

class IfNode(Node):
    def __init__(self, token: Token):
        from tusk.interpreter import Interpreter
        from tusk.nodes.statement import StatementNode
        self.interpreter = token.interpreter
        self.token = token

    async def create(self):
        from tusk.nodes.expressions import ExpressionNode
        from tusk.nodes.statement import StatementNode
        self.condition = await ConditionNode(self.token).create()
        self.interpreter.expect_token("KEYWORD:then")

        self.end_found = False

        self.run_if = self.condition.value
        self.run_else = False

        self.interpreter.debug_msg(self.token,self.run_if, self.interpreter.current_token, "If (node) start")
        self.success = False

        internal_structure_count = 0
        while self.end_found != True:
            self.interpreter.debug_msg(self.token,(self.run_if or self.run_else),internal_structure_count, self.interpreter.current_token, self.interpreter.get_next_token(), "If (node) read")
            nxt_tkn = self.interpreter.get_next_token()
            if nxt_tkn.type=="ENDSTRUCTURE":
                if internal_structure_count == 0:
                    self.interpreter.next_token()
                    self.end_found = True
                    break
                else:
                    internal_structure_count -= 1
                    self.interpreter.next_token()
            elif self.interpreter.is_token("KEYWORD:elseif") and internal_structure_count == 0:
                self.interpreter.next_token()
                if self.run_if == False:
                    self.condition = await ConditionNode(self.interpreter.next_token()).create()
                    if self.condition.value == True:
                        self.interpreter.debug_msg(self.token,self.condition.value,self.success, self.interpreter.current_token, "If (node) elseif")
                        self.interpreter.expect_token("KEYWORD:then")
                        self.run_if = True
                        self.run_else = False
                        self.success = True
                    else: 
                        self.interpreter.debug_msg(self.token,self.condition.value,self.success, self.interpreter.current_token, "If (node) elseif false")
                        self.run_if = False
                        self.run_else = False
                else:
                    self.interpreter.debug_msg(self.token,self.condition,self.success, self.interpreter.current_token, "If (node) elseif already run")
                    self.success = True
                    self.run_if = False
                    self.run_else = False
            elif self.interpreter.is_token("KEYWORD:else") and internal_structure_count == 0:
                self.interpreter.next_token()
                if self.run_if == False and self.success == False:
                    self.run_else = True
                else: 
                    self.run_else = False
                    self.run_if = False
                    self.success = True
            else: 
                e = self.interpreter.next_token()
                
                
                
                if self.run_if or self.run_else:
                    await StatementNode(e).create()
                else:
                    if nxt_tkn.type == "STRUCTURE":
                        internal_structure_count += 1
        self.interpreter.debug_msg(self.token,self.condition.value,self.success, self.interpreter.current_token, "If (node) end")
        return self
       

        
