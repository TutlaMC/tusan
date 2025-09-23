from tusan.Node import *

class ExecuteFunctionNode(Node):
    def __init__(self, token: Token):
        self.interpreter = token.interpreter
        self.token = token

    async def create(self):
        from tusk.nodes.expressions import ExpressionNode
        from tusk.variable import get_type_
        token = self.token
        self.name = token.value
        
        func = token.interpreter.data["funcs"][token.value] # [[], interpreter]
        func_name= token.value
        func_interpreter = func["interpreter"]
        func_params = func["params"]

        
        parased_params = []
        nparams = {}
        for param in func_params: # looping params (func[0] is the param list)
            if param["fallback"] == [None, 5678, "no chance"]: # i had no other idea to get around it so we're doing this list, so if the user by accident provides [None, 5678, "no chance"] they're cooked 💀
                e = self.interpreter.next_token() 

                val = (await ExpressionNode(e).create()).value
                if param["type"] != "ANY":
                    if (await get_type_(val)) == param["type"]:
                        parased_params.append([param["name"],val])
                    else:
                        self.interpreter.error("TypeError", f"Recieved type {(await get_type_(val))} instead of {param['type']} in function {token.value} ") 
                else:
                    parased_params.append([param["name"],val])
            else:
                nparams[param["name"]] = param
        while self.interpreter.get_next_token().value in nparams:
            if nparams[self.interpreter.get_next_token().value]["fallback"] != [None, 5678, "no chance"]:
                self.interpreter.error("SyntaxError",f"What is a required argument ({nparams[self.interpreter.get_next_token().value]['name']}) doing here?")
            else:
                self.interpreter.error("SyntaxError",f"Invalid paramater {self.interpreter.get_next_token().value} in function {token.value}")
            nparams.pop(self.interpreter.get_next_token().value)
        for i in nparams:
            parased_params.append([nparams[i]["name"],nparams[i]["fallback"]])
        

        for i in parased_params: func_interpreter.data["vars"][i[0]] = i[1]

        func_interpreter.data["funcs"] = self.interpreter.data["funcs"]
        self.value = await func_interpreter.compile()
        self.value = func_interpreter.return_value
        return self