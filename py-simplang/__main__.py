import sys
from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):
    KEYWORD = auto()
    COMPARATOR = auto()
    STRING = auto()
    NUMBER = auto()
    DELIMITER = auto()
    IDENTIFIER = auto()

@dataclass
class Token:
    type: TokenType
    literal: str

@dataclass
class FunctionCall:
    name: str
    arguments: list

KEYWORDS = {"if"}

def find_until(string: str, check) -> int:
    """Return the length of match"""
    pos = 0

    while pos < len(string):
        char = string[pos]
        if not check(char):
            return pos
        pos += 1

    return -1


def evaluate_ast(ast):
    for node in ast:
        if isinstance(node, FunctionCall):
            if node.name == "print":
                for arg in node.arguments:
                    print(arg.literal, end=" ")
                print()

def parse_tokens(tokens):
    ast = []
    pos = 0

    while pos < len(tokens):
        token = tokens[pos]

        if token.type == TokenType.IDENTIFIER:
            if not token.literal in KEYWORDS:
                if tokens[pos + 1].type == TokenType.DELIMITER and tokens[pos + 1].literal == "(":
                    name = token.literal
                    args = []
                    pos += 1
                    while pos < len(tokens):
                        if tokens[pos + 1].type == TokenType.DELIMITER and tokens[pos + 1].literal == ")":
                            ast.append(FunctionCall(name, args))
                            break
                        pos += 1
                        
                        if tokens[pos].type == TokenType.DELIMITER and tokens[pos].literal == ",":
                            continue
                        args.append(tokens[pos])

                    pos += 1 # )
        pos += 1

    return ast

def lex_code(code: str):
    pos = 0
    tokens = []

    while pos < len(code):
        cur_char = code[pos]

        if cur_char.isalpha():
            length = find_until(code[pos:], lambda x: x.isalpha())
            match = code[pos:pos+length]
            if match in KEYWORDS:
                tokens.append(Token(TokenType.KEYWORD, match))
            else:
                tokens.append(Token(TokenType.IDENTIFIER, match))
            pos += length - 1
        if cur_char.isdigit():
            length = find_until(code[pos:], lambda x: x.isdigit())
            match = code[pos:pos+length]
            tokens.append(Token(TokenType.NUMBER, match))
            pos += length - 1

        elif cur_char in ('"', "'"):
            length = find_until(code[pos + 1:], lambda x: x not in ('"', "'"))
            if length == -1:
                print("ERROR: Unclosed string found.")
                exit(1)
            match = code[pos + 1:pos+length + 1]
            tokens.append(Token(TokenType.STRING, match))
            pos += length + 1
            
        elif cur_char == "#":
            if code[pos + 1] == "*":
                pos += 2
                while pos < len(code):
                    if code[pos] == "*" and code[pos + 1] == "#":
                        pos += 2
                        break
                    pos += 1
                if pos == len(code):
                    print("ERROR: Unclosed multi-line comment found.")
                    exit(1)
            else:
                length = find_until(code[pos + 1:], lambda x: x != "\n")
                pos += length + 1
        
        elif cur_char in ("(", ")", "[", "]", "{", "}", ",", ";"):
            tokens.append(Token(TokenType.DELIMITER, cur_char))
            
        # todo)) support comparators
        
        pos += 1

    return tokens

def main():
    args = sys.argv[1:]
    
    if len(args) < 1 or args[0] in ("-h", "--help"):
        print(f"Usage: {sys.argv[0]} <filename>")
        exit(1)

    filename = args.pop()

    with open(filename) as file:
        code = file.read()

    tokens = lex_code(code)
    ast = parse_tokens(tokens)
    evaluate_ast(ast)


if __name__ == "__main__":
    main()
