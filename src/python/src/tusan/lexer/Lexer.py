from tusan.lexer.Token import Token
import re

keywords = [
      
      "then", "elseif", "else",
      "that",
      "times","do","as",
      "what","type",
      "characters","items","all",
      "from","of","by","till",
      "capture",
      "get","post","headers","tson",
      "character","item","number",
      "file", "variable", 
      "with","between",
      "named",
      "for", "can",
      "a", "an", "the","so","to",
      "toall",
      "can","cannot",
      "because",
]

types = ["NUMBER","STRING","BOOL","BOOLEAN","LIST","NOTHING","TSON"]

EFFECTS = [
    "set",
    "print",
    "wait",
    "add","remove","split","replace", 
    "length",
    "input","convert",
    "shell",
    "request",
    "index",
    "read","write","rename",
    "delete",
    "random",
    "import",
]

STRUCTURES = [
    "if","while","function","loop"
]

# May not be the best lexer, but hey- if it works it works and don't touch it, you'll prob mess it up

default_token_classification = {
    "STRING": r"(['\"])(?:\\.|(?!\1).)*\1", 
    "NUMBER": r"-?\d+(\.\d+)?",
    "BOOLEAN": r"\b(true|false)\b",
    "NULL": r"\bnothing\b",

    "LEFT_PAR": r"\(",
    "RIGHT_PAR": r"\)",
    "LEFT_CURLY": r"\{",
    "RIGHT_CURLY": r"\}",
    "LEFT_SQUARE": r"\[",
    "RIGHT_SQUARE": r"\]",
    "COMMA": r",",
    "SEMICOLON": r";",
    "COLON": r":",

    "ADD": r"\+",
    "SUBTRACT": r"-",
    "MULTIPLY": r"(?<!\*)\*(?!\*)",
    "EXPONENT": r"(?<!\*)\*\*(?!\*)",
    "DIVIDE": r"/",
    "MODULO": r"%",

    "RETURN": r"\breturn\b",
    "BREAK": r"\bbreak\b",
    "END": r"\bend\b",

    "AND": r"\b(and)\b|(?<!&)&&(?!!)",
    "OR": r"\b(or)\b|(?<!\|)\|\|(?!\|)",
    "EQUALITY": r"==|is",
    "NOT_EQUALS": r"!=",
    "NOT": r"!|\bnot\b",
    "OWNERSHIP": r"\bin\b|\bcontains\b",
    "GREATER": r">",
    "LESSER": r"<",
    "GOE": r">=",
    "LOE": r"<=",
    "IGNORE": r"#.*",

    "ASSIGN": r"(\b(to|be)\b)|=",

    "KEYWORD": keywords,
    "TYPE": types,
    "EFFECT": EFFECTS,
    "STRUCTURE": STRUCTURES,
    "IDENTIFIER": r"[A-Za-z_][A-Za-z0-9_]*",
}



class Lexer:
    def __init__(self,text, interpreter):
        self.text = text

        self.token_classification = default_token_classification

        self.pos = 0
        self.current_token = None

        self.tokens = []

        self.interpreter = interpreter

    def set_classifications(self, classification):
        self.token_classification = classification
      
    def reg(self, name, value):
        self.tokens.append(Token(name.upper(), value, self.interpreter))
        self.ctoken = ""
    
    def tokenize(self):
        index = 0
        length = len(self.text)

        while index < length:
            match_found = False
            while index < length and self.text[index].isspace():
                index += 1

            if index >= length:
                break

            ignore_patterns = self.token_classification.get("IGNORE", [])
            if isinstance(ignore_patterns, list):
                for p in ignore_patterns:
                    regex = re.compile(p, re.MULTILINE)
                    m = regex.match(self.text, index)
                    if m:
                        index = m.end()  
                        match_found = True
                        break
            else:
                regex = re.compile(ignore_patterns, re.MULTILINE)
                m = regex.match(self.text, index)
                if m:
                    index = m.end()
                    match_found = True

            if match_found:
                continue

            for token_type, pattern in self.token_classification.items():
                if token_type == "IGNORE":
                    continue

                if isinstance(pattern, list): 
                    for word in pattern:
                        end = index + len(word)
                        if self.text[index:end] == word and (end == length or not self.text[end].isalnum()):
                            self.reg(token_type, word)
                            index = end
                            match_found = True
                            break
                    if match_found:
                        break
                else:
                    regex = re.compile(pattern)
                    m = regex.match(self.text, index)
                    if m:
                        self.reg(token_type, m.group())
                        index = m.end()
                        match_found = True
                        break

            if not match_found: # eh i had no other idea, maybe config for another day
                self.reg("IDENTIFIER", self.text[index])
                index += 1

        self.reg("ENDSCRIPT", "")