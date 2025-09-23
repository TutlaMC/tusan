JAVASCRIPT_COMMENTS = [
    r"//.*",         # JS single-line
    r"/\*[\s\S]*?\*/"  # JS multi-line
]

PYTHON_COMMENT r"#.*"

# old classifications
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